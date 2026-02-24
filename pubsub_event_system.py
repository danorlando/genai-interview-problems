from typing import Dict, List, Any, Callable


class Event:
    topic: str
    data: Dict[str, Any]
    timestamp: float
    metadata: Dict[str, Any]


class EventBus:
    
    pass





if __name__ == "__main__":
    import time
    
    print("=" * 60)
    print("Event Bus Demo")
    print("=" * 60)
    
    # Create EventBus instance
    bus = EventBus()
    
    # Define handler functions
    def high_priority_handler(event: Event):
        print(f"  [HIGH PRIORITY] Handling {event.topic}: {event.data}")
    
    def medium_priority_handler(event: Event):
        print(f"  [MEDIUM PRIORITY] Handling {event.topic}: {event.data}")
    
    def low_priority_handler(event: Event):
        print(f"  [LOW PRIORITY] Handling {event.topic}: {event.data}")
    
    def llm_wildcard_handler(event: Event):
        print(f"  [WILDCARD llm.*] Caught {event.topic}: {event.data}")
    
    def error_handler(event: Event):
        print(f"  [ERROR HANDLER] About to raise exception...")
        raise ValueError("Intentional error for demo!")
    
    def cleanup_handler(event: Event):
        print(f"  [CLEANUP] This runs even after errors: {event.topic}")
    
    # Demo 1: Priority ordering
    print("\n1. PRIORITY ORDERING DEMO")
    print("-" * 60)
    bus.subscribe("model.start", low_priority_handler, priority=-10)
    bus.subscribe("model.start", high_priority_handler, priority=10)
    bus.subscribe("model.start", medium_priority_handler, priority=0)
    
    event1 = Event()
    event1.topic = "model.start"
    event1.data = {"model": "gpt-4", "action": "starting"}
    event1.timestamp = time.time()
    event1.metadata = {}
    
    count = bus.publish("model.start", event1)
    print(f"Handlers called: {count}")
    
    # Demo 2: Wildcard subscriptions
    print("\n2. WILDCARD SUBSCRIPTIONS DEMO")
    print("-" * 60)
    print("Note: Subscribing to llm.start, llm.complete, llm.error")
    bus.subscribe("llm.start", llm_wildcard_handler, priority=5)
    bus.subscribe("llm.complete", llm_wildcard_handler, priority=5)
    bus.subscribe("llm.error", llm_wildcard_handler, priority=5)
    
    event2 = Event()
    event2.topic = "llm.start"
    event2.data = {"prompt": "Hello world"}
    event2.timestamp = time.time()
    event2.metadata = {"trace_id": "abc123"}
    
    event3 = Event()
    event3.topic = "llm.complete"
    event3.data = {"response": "Hello! How can I help?"}
    event3.timestamp = time.time()
    event3.metadata = {"trace_id": "abc123"}
    
    bus.publish("llm.start", event2)
    bus.publish("llm.complete", event3)
    
    # Demo 3: Multiple events with different payloads
    print("\n3. DIFFERENT EVENT PAYLOADS DEMO")
    print("-" * 60)
    
    def data_handler(event: Event):
        print(f"  Processing {event.topic} with keys: {list(event.data.keys())}")
    
    bus.subscribe("data.received", data_handler)
    
    event4 = Event()
    event4.topic = "data.received"
    event4.data = {"user_id": 123, "action": "login", "ip": "192.168.1.1"}
    event4.timestamp = time.time()
    event4.metadata = {}
    
    event5 = Event()
    event5.topic = "data.received"
    event5.data = {"temperature": 72.5, "humidity": 45, "location": "office"}
    event5.timestamp = time.time()
    event5.metadata = {}
    
    bus.publish("data.received", event4)
    bus.publish("data.received", event5)
    
    # Demo 4: Unsubscribe functionality
    print("\n4. UNSUBSCRIBE DEMO")
    print("-" * 60)
    
    def temp_handler(event: Event):
        print(f"  Temporary handler: {event.data}")
    
    bus.subscribe("temp.topic", temp_handler)
    print(f"Subscriber count before unsubscribe: {bus.get_subscriber_count('temp.topic')}")
    
    event6 = Event()
    event6.topic = "temp.topic"
    event6.data = {"message": "First publish"}
    event6.timestamp = time.time()
    event6.metadata = {}
    
    bus.publish("temp.topic", event6)
    
    success = bus.unsubscribe("temp.topic", temp_handler)
    print(f"Unsubscribe successful: {success}")
    print(f"Subscriber count after unsubscribe: {bus.get_subscriber_count('temp.topic')}")
    
    event7 = Event()
    event7.topic = "temp.topic"
    event7.data = {"message": "Second publish (no handlers)"}
    event7.timestamp = time.time()
    event7.metadata = {}
    
    count = bus.publish("temp.topic", event7)
    print(f"Handlers called: {count}")
    
    # Demo 5: Exception handling
    print("\n5. EXCEPTION HANDLING DEMO")
    print("-" * 60)
    print("Showing that one handler's exception doesn't break others...")
    
    bus.subscribe("error.test", high_priority_handler, priority=10)
    bus.subscribe("error.test", error_handler, priority=5)
    bus.subscribe("error.test", cleanup_handler, priority=0)
    
    event8 = Event()
    event8.topic = "error.test"
    event8.data = {"test": "exception handling"}
    event8.timestamp = time.time()
    event8.metadata = {}
    
    count = bus.publish("error.test", event8)
    print(f"Total handlers called: {count} (all executed despite error)")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)