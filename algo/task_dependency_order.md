## Problem Statement
You are given a list of tasks that need to be executed. Each task has a name and a list of dependencies that must be completed before the task can be executed. Some tasks may depend on multiple other tasks.

## Task Object
The Task object has the following structure:
```
Task {
  name: string;
  dependencies: string[];  // List of task names that must be completed before this task
}
```

## Requirements
1. Write a function that takes an array of task names as input.
2. The function should return an ordered list of all tasks that need to be executed, including both the input tasks and their dependencies.
3. Tasks should appear in the order they need to be executed. A task can only be executed after all its dependencies have been executed.
4. If there are circular dependencies, your function should detect them and throw an error.

## Example
Input:
```
["frontend_deploy", "backend_deploy"]
```

Task definitions (this would be available as some kind of lookup):
```
{
  "frontend_install": { dependencies: [] },
  "frontend_lint": { dependencies: ["frontend_install"] },
  "frontend_test": { dependencies: ["frontend_install", "shared_build"] },
  "frontend_build": { dependencies: ["frontend_lint", "frontend_test", "shared_build"] },
  "frontend_deploy": { dependencies: ["frontend_build", "backend_build"] },
  
  "backend_install": { dependencies: [] },
  "backend_lint": { dependencies: ["backend_install"] },
  "backend_test": { dependencies: ["backend_install", "database_setup", "shared_build"] },
  "backend_build": { dependencies: ["backend_lint", "backend_test"] },
  "backend_deploy": { dependencies: ["backend_build", "database_migrate"] },
  
  "shared_install": { dependencies: [] },
  "shared_test": { dependencies: ["shared_install"] },
  "shared_build": { dependencies: ["shared_test"] },
  
  "database_setup": { dependencies: [] },
  "database_migrate": { dependencies: ["database_setup", "backend_build"] }
}
```

Expected Output (one possible correct ordering):
```
["shared_install", "shared_test", "shared_build", "frontend_install", "frontend_lint", "backend_install", "backend_lint", "database_setup", "backend_test", "backend_build", "database_migrate", "frontend_test", "frontend_build", "frontend_deploy", "backend_deploy"]
```

## Constraints
- There can be between 1 and 100 tasks in the input array.
- Task names are unique strings.
- Task dependencies will always refer to valid task names.
- Multiple valid orderings may exist. Your function should return any valid ordering.
- The input will be valid JSON.

