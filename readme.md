# Twitter Reloaded - A small message app built on python 

This repository showcases the final project of Arquitecture and Software Design - 551- 2023 

## Design Patterns

### Factory Design Pattern

The `DataStoreFactory` class implements the Factory design pattern. It provides a static method `create_data_store()` that creates and returns an instance of the `DataStore` class. This encapsulates the creation logic and provides a centralized place for creating `DataStore` objects. It promotes loose coupling by allowing the creation of `DataStore` objects without explicitly specifying their concrete class.

### Singleton Design Pattern

The `DataStore` class can be considered an implementation of the Singleton design pattern. Although it doesn't enforce the restriction of having only one instance, it provides a centralized data storage mechanism through its static methods `load_data()` and `save_data()`. These methods access a shared data file (`events.json` and `messages.json`) and ensure that the data is consistent across different instances of the `DataStore` class. By using the same data store, multiple components can access and modify the data consistently.

### Observer Design Pattern

The Observer class and its subclasses (`UserEventManager` and `MessageEventManager`) implement the Observer design pattern. The `Observer` class provides the infrastructure for registering observers, storing them in a list, and notifying them when certain events occur. The `EventManager` class extends the `Observer` class and uses the `register_observer()` and `notify_observers()` methods to register and notify observers when events are registered.

In this project, the `UserEventManager` and `MessageEventManager` classes are observers that register with the `EventManager`. They are notified whenever events are registered, and they can perform their specific tasks accordingly. The `EventManagerTests` class also serves as an observer, as it registers itself with the `EventManager` to receive notifications and perform test assertions based on the observed events.

## SOLID Principles

### Single Responsibility Principle (SRP)

The classes in this project adhere to the Single Responsibility Principle by focusing on specific responsibilities:

- The `Observer` class focuses on managing and notifying observers.
- The `DataStore` class handles data loading and saving operations.
- The `EventManager` class manages events and performs related operations.
- The `MessageManager` class handles message-related functionalities.
- The `UserManager` class manages user-related operations.

### Open-Closed Principle (OCP)

The `EventManager` class is open for extension, enabling the creation of specialized event managers such as `UserEventManager` and `MessageEventManager`. New event types can be added by extending the event manager.

### Liskov Substitution Principle (LSP)

The subclasses `UserEventManager` and `MessageEventManager` inherit from the `EventManager` class without altering its behavior, adhering to the Liskov Substitution Principle.

### Interface Segregation Principle (ISP)

Although explicit interfaces are not defined, the `EventManager` class serves as an interface for registering events and notifying observers. The subclasses, `UserEventManager` and `MessageEventManager`, implement specific event registration methods, adhering to the Interface Segregation Principle.

### Dependency Inversion Principle (DIP)

The `EventManager` class depends on abstractions (`Observer`) rather than concrete implementations to register and notify observers. This promotes decoupling and flexibility between the event manager and its observers.

Feel free to explore the code and dive deeper into the implementation of these patterns and principles!
