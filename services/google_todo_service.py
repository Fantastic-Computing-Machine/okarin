import os
import pickle  # For storing token
from google.adk.agents import Agent
from google.genai import types
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from services.google_cred_service import get_google_credentials

SCOPES = ["https://www.googleapis.com/auth/tasks"]
TOKEN_PICKLE_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"

_task_list_cache = None
_task_id_map_cache = None


def get_tasks_service():
    creds = get_google_credentials(SCOPES)
    try:
        service = build("tasks", "v1", credentials=creds)
        return service
    except Exception as e:
        print(f"An error occurred building the service: {e}")
        raise


def _fetch_and_cache_tasks(service):
    """Helper to fetch tasks and populate caches."""
    global _task_list_cache, _task_id_map_cache
    _task_list_cache = []
    _task_id_map_cache = {}
    try:
        results = (
            service.tasks()
            .list(
                tasklist="@default",
                showCompleted=False,
                showHidden=False,
                maxResults=100,
            )
            .execute()
        )
        items = results.get("items", [])
        if items:
            for i, task_item in enumerate(items):
                if task_item.get("status") != "completed":
                    _task_list_cache.append(
                        {
                            "id": task_item["id"],  # Google's Task ID
                            "title": task_item["title"],
                            "notes": task_item.get("notes", ""),
                        }
                    )
                    _task_id_map_cache[i + 1] = task_item[
                        "id"
                    ]  # Map 1, 2, 3... to Google ID
        return items
    except HttpError as err:
        print(f"An API error occurred while fetching tasks: {err}")
        return []


def list_tasks() -> str:
    """Lists all current, non-completed tasks from Google Tasks with a simple numeric ID for user interaction."""
    global _task_list_cache, _task_id_map_cache
    service = get_tasks_service()
    _fetch_and_cache_tasks(service)  # Refresh cache

    if not _task_list_cache:
        return "Your Google Tasks list is empty or all tasks are completed."

    output = "Your Google To-Do List (pending tasks):\n"
    for i, task in enumerate(_task_list_cache):
        output += f"{i + 1}. {task['title']}\n"  # User sees 1, 2, 3...
    output += "\nUse the number to refer to tasks for completion."
    return output.strip()


def add_task(description: str) -> str:
    """Adds a new task to the default Google Tasks list."""
    global _task_list_cache  # Invalidate cache
    service = get_tasks_service()
    task_body = {
        "title": description,
    }
    try:
        created_task = (
            service.tasks().insert(tasklist="@default", body=task_body).execute()
        )
        _task_list_cache = None  # Invalidate cache as list has changed
        return (
            f"Task '{description}' added to Google Tasks with ID {created_task['id']}."
        )
    except HttpError as err:
        print(f"An API error occurred while adding task: {err}")
        return f"Error adding task '{description}' to Google Tasks. Please check logs."


def complete_task(task_number: int) -> str:
    """
    Marks a task as complete in Google Tasks given its simple numeric ID from the list_tasks command.
    """
    global _task_list_cache, _task_id_map_cache
    service = get_tasks_service()
    if not _task_id_map_cache:
        _fetch_and_cache_tasks(service)
        if not _task_id_map_cache:
            return "Could not find tasks to complete. Please list tasks first."

    google_task_id = _task_id_map_cache.get(task_number)

    if not google_task_id:
        return f"Error: Task number {task_number} not found in the current list. Please use 'list_tasks' to see available task numbers."

    try:
        task_to_complete = (
            service.tasks().get(tasklist="@default", task=google_task_id).execute()
        )
        task_title = task_to_complete.get("title", "Unknown Task")

        if task_to_complete.get("status") == "completed":
            return f"Task '{task_title}' (ID: {google_task_id}) is already completed."

        updated_task_body = {"id": google_task_id, "status": "completed"}
        service.tasks().update(
            tasklist="@default", task=google_task_id, body=updated_task_body
        ).execute()
        _task_list_cache = None
        _task_id_map_cache = None
        return f"Task '{task_title}' (ID: {google_task_id}) has been marked as completed in Google Tasks."
    except HttpError as err:
        if err.resp.status == 404:
            return f"Error: Task with Google ID {google_task_id} (number {task_number}) not found in Google Tasks."
        print(f"An API error occurred while completing task: {err}")
        return f"Error completing task number {task_number}. Please check logs."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return (
            f"An unexpected error occurred while completing task number {task_number}."
        )


def get_tools():
    return [
        list_tasks,
        add_task,
        complete_task,
    ]
