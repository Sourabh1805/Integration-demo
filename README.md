# Integration 

**Note:** Please do not put your solution in a public repository (GitHub etc.). We are sending this to multiple candidates and do not want anyone to have an unfair advantage.

## Setup

* Install Python 3.11+.
* Install SQLite. Mac already has this installed already most of the time.
* `git clone` the repository.
* Create a virtualenv.
* `pip install -r requirements`.

## Running

* Start OurAPI:
  * `cd our_api`
  * `uvicorn main:app --port 8266` (inside virtualenv) 
* Start BigChat:
  * `cd big_chat`
  * `uvicorn main:app --port 8267` (inside virtualenv) 

## BigChat API

BigChat is a fake live chat service. It's API returns one of four events:

* `START`: When a chat starts.
* `END`: When a chat ends.
* `MESSAGE`: When a customer or agent sends a message.
* `TRANSFER`: When a chat is transferred from one agent to another.

When the app is running, you can find the documentation here: http://127.0.0.1:8267/docs.

## Our API

When the app is running, you can find the documentation here: http://127.0.0.1:8266/docs.

## Task

Create an integration between BigChat API and Our API. Write a script that calls BigChat's `/events` route every 10 seconds (to get the latest events in the last 10 seconds) that will create/edit chats and agents in OurAPI as needed. Feel free to edit anything inside `/integration`. Add as many files or whatever structure you want. We would recommend writing tests as well.

Please do not edit anything inside `/big_chat` or `/our_api`, assume they are APIs that can't be changed.


# Solution 
## Key Focus Areas

**Demonstrated SDLC Lifecycle Events:**

Followed a structured approach to requirements, design, implementation, and testing.

**Reliable Solution:**

  Prioritized system reliability even with unpredictable BigChat event behavior.

**Scalable Architecture:**

  Designed a modular, scalable architecture to accommodate future enhancements.

**SOLID Principles:**

  Ensured maintainable and extensible code by adhering to SOLID principles.

**Design Patterns:**

  Implemented Singleton for database connections and logging.

### start event 
    Process:
        1. Retrieve conversation details using the conversation ID from the event.
        2. Fetch advisor details associated with the conversation.
        3. Verify if the agent for the advisor exists:
            - If no agent exists, create a new agent.
            - If one agent exists, use it.
            - If multiple agents exist, log a warning.
        4. Convert the `event_at` time from the conversation details to a proper datetime string.
        5. Start a new event using the agent and conversation details.
        6. Create a new chat service to save the event in the database.
        7. Log success or failure of the operation:
            - Log if the event was successfully saved.
            - Log a warning if there were any issues.

### end event
    end_time (str): The timestamp marking the end of the event, in string format.

    Process:
        1. Retrieve conversation details using the conversation ID.
        2. Fetch advisor details associated with the conversation.
        3. Verify if the agent for the advisor exists:
            - If no agent exists, create a new agent.
            - If one agent exists, use it.
            - If multiple agents exist, log a warning.
        4. Convert the `event_at` time from the first conversation event to a proper datetime string.
        5. Use the agent and conversation details to trigger an "end event" in the system.
        6. Create or update the chat event in the database with the provided details.
        7. Log success or failure of the operation:
            - Log if the event was successfully saved.
            - Log a warning if there was an issue. 

### message event
    Process:
        1. Retrieve conversation details using the conversation ID.
        2. Fetch advisor details associated with the conversation.
        3. Verify if the agent for the advisor exists:
            - If no agent exists, create a new agent.
            - If one agent exists, use it.
            - If multiple agents exist, log a warning.
        4. Convert the `event_at` time to a proper datetime string.
        5. Start a new chat event using the agent and conversation details.
        6. Send a message through the message service API.
        7. Log success or failure of the message event:
            - On success, save the event in the database.
            - On failure, log an appropriate warning.

### Transfer event
    Process:
        1. Retrieves and logs the conversation details using the conversation ID.
        2. Fetches and verifies the current advisor and associated agent details:
            - Creates a new agent if none exists.
        3. Converts the event timestamp to a proper datetime format.
        4. Initiates a chat event using the current advisor and agent.
        5. Handles the transfer to a new advisor:
            - Verifies the existence of the transfer advisor and their agent.
            - Creates a new agent if none exists.
        6. Initiates a transfer event with the new agent.
        7. Logs the success or failure of the transfer and updates the database.

## Testing
`pytest -v test/test_handler/test_all_events_handler.py`

## Git Workflow
Branches:

  dev: Active development branch.

  test: For testing features and bug fixes.

  main: Stable production-ready branch.


# Challenges Faced

**OurAPI /chats Instability:**

  The OurAPI would intermittently shut down, requiring a manual restart. This was mitigated by restarting the API and logging the error.

**BigChat Event Behavior:**

  BigChat API emitted unpredictable events, often resetting during testing. This made testing event reliability more complex.

**Testing Challenges:**

  Started with mock-based pytest, but mocking was not the best approach for end-to-end testing due to the dynamic nature of the APIs.
  Due to time constraints, testing was scoped down to focus on critical paths.

## Future Enhancements

**Detailed Testing:**

  Write additional test cases to cover edge cases and scenarios.
  Mock failure scenarios (e.g., Our API returns 404 or 500) and validate retry mechanisms.

**Retry Mechanism for Failed Events:**

  Save failed events (e.g., Our API /chats returns 404) in the database.
  Implement a background process to retry failed events periodically.
