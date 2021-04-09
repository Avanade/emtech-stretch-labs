# Technical Architecture
[Diagram of architecture](codegen/technical_architecture.png)

- Unity Application with Nextmind in C# calls Python App
- Python App forwards API calls to Rocos
- Rocos interacts with stretch


## Why have the Python App in the middle?
Mainly for debugging, and in case we were running more than 1 robot, we could track the messages going to and from.