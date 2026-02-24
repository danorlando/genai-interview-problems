Exercise: Pub-Sub Event System

Description

Build an event-driven publish-subscribe system that implements the Observer pattern. This is fundamental to building reactive systems, especially in GenAI applications where you need to handle events like model completions, streaming responses, or pipeline stage notifications.

Requirements

Classes to implement:

**EventBus**
- `subscribe(topic: str, handler: Callable, priority: int = 0)`: Registers handler for topic. Higher priority executes first.
- `unsubscribe(topic: str, handler: Callable) -> bool`: Removes handler from topic. Returns success status.
- `publish(topic: str, event: Event) -> int`: Publishes event to all subscribers. Returns count of handlers called.
- `publish_async(topic: str, event: Event) -> None`: Publishes without waiting for handlers (fire-and-forget).
- `get_subscriber_count(topic: str) -> int`: Returns number of subscribers for topic.
- `clear_topic(topic: str) -> int`: Removes all subscribers from topic. Returns count removed.

**Event** (data class or class)
- `topic: str` - event topic
- `data: Dict[str, Any]` - event payload
- `timestamp: float` - when event was created
- `metadata: Dict[str, Any]` - optional metadata (publisher info, trace ID, etc.)

Behavior:
- Handlers are called in priority order (high to low), then subscription order for same priority.
- Support wildcard subscriptions: "model.*" subscribes to "model.start", "model.complete", etc.
- If a handler raises an exception, log it but continue calling remaining handlers.
- Handlers receive Event object as single argument.
- Support multiple handlers per topic with different priorities.

Implementation Notes:
- Use defaultdict or similar for topic -> handlers mapping.
- Consider using a heap or sorted list for priority handling.
- Wildcard matching can use fnmatch or simple string operations.
- Think about handler signature validation (should accept Event).

Deliverable (pubsub_event_system.py)

The EventBus and Event implementations with:
- Clean Observer pattern implementation
- Efficient priority-based handler execution
- Proper wildcard topic matching
- Exception handling for handler failures
- Type hints for all methods

