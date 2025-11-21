#!/usr/bin/env python3
"""Test script for the enhanced GitHub Reader tool."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent.tools.github_reader import GitHubReader

def test_github_reader():
    """Test the GitHub Reader functionality."""
    
    # Initialize the reader with project root
    project_root = Path(__file__).parent
    reader = GitHubReader(project_root=str(project_root))
    
    print("=" * 80)
    print("Testing GitHub Reader Tool")
    print("=" * 80)
    
    # Test with a small public repository
    test_repo = "https://github.com/octocat/Hello-World"
    
    print(f"\n1. Testing clone_repo() with: {test_repo}")
    print("-" * 80)
    clone_result = reader.clone_repo(test_repo)
    print(f"Status: {clone_result['status']}")
    print(f"Message: {clone_result['message']}")
    print(f"Clone Path: {clone_result['clone_path']}")
    
    if clone_result['status'] in ['success', 'exists']:
        print(f"\n2. Testing analyze_cloned_repo()")
        print("-" * 80)
        analysis = reader.analyze_cloned_repo(test_repo)
        
        if analysis['status'] == 'success':
            print(f"Owner: {analysis['owner']}")
            print(f"Repo: {analysis['repo']}")
            print(f"Clone Path: {analysis['clone_path']}")
            print(f"\nStatistics:")
            print(f"  - Total Files: {analysis['stats']['total_files']}")
            print(f"  - Total Directories: {analysis['stats']['total_dirs']}")
            print(f"  - Total Size: {analysis['stats']['total_size_bytes']:,} bytes")
            
            if analysis['key_files']:
                print(f"\nKey Files Found:")
                for filename in analysis['key_files'].keys():
                    print(f"  - {filename}")
            
            print(f"\nDirectory Structure (first 20 items):")
            for item in analysis['structure'][:20]:
                print(f"  {item}")
        else:
            print(f"Error: {analysis['message']}")
        
        print(f"\n3. Testing read_repo() (high-level method)")
        print("-" * 80)
        summary = reader.read_repo(test_repo, use_clone=True)
        print(summary)
        
        print(f"\n4. Testing cleanup_repo()")
        print("-" * 80)
        cleanup_result = reader.cleanup_repo(test_repo)
        print(f"Status: {cleanup_result['status']}")
        print(f"Message: {cleanup_result['message']}")
    
    print("\n" + "=" * 80)
    print("Test completed!")
    print("=" * 80)

if __name__ == "__main__":
    test_github_reader()
