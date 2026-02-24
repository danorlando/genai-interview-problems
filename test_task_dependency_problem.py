import unittest
from typing import List, Dict, Set
from collections import defaultdict

from task_dependency_order import order_tasks

# Example Task class definition (for reference)
class Task:
    def __init__(self, name: str, dependencies: List[str] = None):
        self.name = name
        self.dependencies = dependencies or []

# Test cases
class TestTaskDependencies(unittest.TestCase):
    
    def validate_ordering(self, result: List[str], task_map: Dict[str, Task]) -> bool:
        """Helper method to validate if the ordering is correct"""
        completed = set()
        
        for task_name in result:
            # Get dependencies for this task
            deps = task_map[task_name].dependencies
            
            # Check if all dependencies are completed
            for dep in deps:
                if dep not in completed:
                    return False
            
            # Mark this task as completed
            completed.add(task_name)
        
        return True
    
    def test_linear_chain(self):
        """Test a simple linear chain of dependencies"""
        task_map = {
            "task_A": Task("task_A", []),
            "task_B": Task("task_B", ["task_A"]),
            "task_C": Task("task_C", ["task_B"]),
            "task_D": Task("task_D", ["task_C"])
        }
        
        result = order_tasks(["task_D"], task_map)
        
        # Check all tasks are included
        self.assertEqual(set(result), {"task_A", "task_B", "task_C", "task_D"})
        
        # Check ordering is valid
        self.assertTrue(self.validate_ordering(result, task_map))
        
        # Check specific expected order for this simple case
        self.assertEqual(result, ["task_A", "task_B", "task_C", "task_D"])
    
    def test_multiple_independent_tasks(self):
        """Test multiple independent tasks with no dependencies"""
        task_map = {
            "task_A": Task("task_A", []),
            "task_B": Task("task_B", []),
            "task_C": Task("task_C", [])
        }
        
        result = order_tasks(["task_A", "task_B", "task_C"], task_map)
        
        # Check all tasks are included
        self.assertEqual(set(result), {"task_A", "task_B", "task_C"})
        
        # Check ordering is valid (any order is valid in this case)
        self.assertTrue(self.validate_ordering(result, task_map))
    
    def test_diamond_dependency(self):
        """Test a diamond-shaped dependency graph"""
        task_map = {
            "task_A": Task("task_A", []),
            "task_B": Task("task_B", ["task_A"]),
            "task_C": Task("task_C", ["task_A"]),
            "task_D": Task("task_D", ["task_B", "task_C"])
        }
        
        result = order_tasks(["task_D"], task_map)
        
        # Check all tasks are included
        self.assertEqual(set(result), {"task_A", "task_B", "task_C", "task_D"})
        
        # Check ordering is valid
        self.assertTrue(self.validate_ordering(result, task_map))
        
        # Check task_A comes before task_B and task_C
        self.assertTrue(result.index("task_A") < result.index("task_B"))
        self.assertTrue(result.index("task_A") < result.index("task_C"))
        
        # Check task_B and task_C come before task_D
        self.assertTrue(result.index("task_B") < result.index("task_D"))
        self.assertTrue(result.index("task_C") < result.index("task_D"))
    
    def test_complex_graph(self):
        """Test a complex graph with multiple entry points"""
        task_map = {
            "task_A": Task("task_A", []),
            "task_B": Task("task_B", ["task_A"]),
            "task_C": Task("task_C", ["task_A"]),
            "task_D": Task("task_D", ["task_B", "task_C"]),
            "task_E": Task("task_E", []),
            "task_F": Task("task_F", ["task_E"]),
            "task_G": Task("task_G", ["task_E", "task_D"]),
            "task_X": Task("task_X", ["task_D", "task_F"]),
            "task_Y": Task("task_Y", ["task_G"])
        }
        
        result = order_tasks(["task_X", "task_Y"], task_map)
        
        # Check all required tasks are included
        expected_tasks = {"task_A", "task_B", "task_C", "task_D", "task_E", 
                         "task_F", "task_G", "task_X", "task_Y"}
        self.assertEqual(set(result), expected_tasks)
        
        # Check ordering is valid
        self.assertTrue(self.validate_ordering(result, task_map))
    
    def test_circular_dependency(self):
        """Test detection of circular dependencies"""
        task_map = {
            "task_A": Task("task_A", ["task_C"]),
            "task_B": Task("task_B", ["task_A"]),
            "task_C": Task("task_C", ["task_B"])
        }
        
        # Expect an exception for circular dependency
        with self.assertRaises(Exception):
            order_tasks(["task_C"], task_map)
    
    def test_complex_circular_dependency(self):
        """Test detection of more complex circular dependencies"""
        task_map = {
            "task_A": Task("task_A", []),
            "task_B": Task("task_B", ["task_A"]),
            "task_C": Task("task_C", ["task_B"]),
            "task_D": Task("task_D", ["task_C", "task_E"]),
            "task_E": Task("task_E", ["task_D"])
        }
        
        # Expect an exception for circular dependency
        with self.assertRaises(Exception):
            order_tasks(["task_E"], task_map)
    
    def test_original_problem(self):
        """Test the original problem example"""
        task_map = {
            "frontend_install": Task("frontend_install", []),
            "frontend_lint": Task("frontend_lint", ["frontend_install"]),
            "frontend_test": Task("frontend_test", ["frontend_install", "shared_build"]),
            "frontend_build": Task("frontend_build", ["frontend_lint", "frontend_test", "shared_build"]),
            "frontend_deploy": Task("frontend_deploy", ["frontend_build", "backend_build"]),
            
            "backend_install": Task("backend_install", []),
            "backend_lint": Task("backend_lint", ["backend_install"]),
            "backend_test": Task("backend_test", ["backend_install", "database_setup", "shared_build"]),
            "backend_build": Task("backend_build", ["backend_lint", "backend_test"]),
            "backend_deploy": Task("backend_deploy", ["backend_build", "database_migrate"]),
            
            "shared_install": Task("shared_install", []),
            "shared_test": Task("shared_test", ["shared_install"]),
            "shared_build": Task("shared_build", ["shared_test"]),
            
            "database_setup": Task("database_setup", []),
            "database_migrate": Task("database_migrate", ["database_setup", "backend_build"])
        }
        
        result = order_tasks(["frontend_deploy", "backend_deploy"], task_map)
        
        # Check all tasks are included
        expected_tasks = set(task_map.keys())
        self.assertEqual(set(result), expected_tasks)
        
        # Check ordering is valid
        self.assertTrue(self.validate_ordering(result, task_map))

if __name__ == "__main__":
    unittest.main()