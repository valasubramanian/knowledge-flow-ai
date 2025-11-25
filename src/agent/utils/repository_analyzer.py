"""Repository Analyzer - Utility for analyzing cloned GitHub repositories."""

import os
from pathlib import Path
from typing import Dict, List, Optional

class RepositoryAnalyzer:
    """Helper class for analyzing cloned repositories."""
    
    def __init__(self):
        """Initialize the analyzer with the temp directory path."""
        self.temp_dir = Path(os.getcwd()) / "temp" / "github_clones"
    
    def _parse_repo_url(self, repo_url: str) -> tuple[str, str]:
        """Parse GitHub URL to extract owner and repo name.
        
        Args:
            repo_url: GitHub repository URL (HTTPS or SSH)
            
        Returns:
            Tuple of (owner, repo_name)
            
        Raises:
            ValueError: If URL is invalid
        """
        # Remove .git suffix if present
        repo_url = repo_url.rstrip("/").replace(".git", "")
        
        # Handle HTTPS URLs: https://github.com/owner/repo
        if "github.com/" in repo_url:
            parts = repo_url.split("github.com/")[-1].split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]
        
        # Handle SSH URLs: git@github.com:owner/repo
        if "git@github.com:" in repo_url:
            parts = repo_url.split("git@github.com:")[-1].split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]
        
        raise ValueError(f"Invalid GitHub URL: {repo_url}")
    
    def get_clone_path(self, repo_url: str) -> Optional[Path]:
        """Get the clone path for a repository URL."""
        try:
            owner, repo = self._parse_repo_url(repo_url)
            clone_path = self.temp_dir / owner / repo
            return clone_path if clone_path.exists() else None
        except:
            return None
    
    def analyze_structure(self, repo_url: str) -> str:
        """Analyze repository structure and provide overview.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            String with repository structure analysis
        """
        clone_path = self.get_clone_path(repo_url)
        if not clone_path:
            return "Error: Repository not cloned. Please clone it first using clone_repo tool."
        
        try:
            # Get basic stats
            stats = self._get_repo_stats(clone_path)
            
            # Get directory structure
            structure = self._get_directory_structure(clone_path, max_depth=3)
            
            # Read key files
            key_files = self._read_key_files(clone_path)
            
            # Detect programming languages
            languages = self._detect_languages(clone_path)
            
            # Format output
            output = f"Repository Structure Analysis\n"
            output += f"=" * 50 + "\n\n"
            output += f"Location: {clone_path}\n\n"
            
            output += f"Statistics:\n"
            output += f"  - Total Files: {stats['total_files']}\n"
            output += f"  - Total Directories: {stats['total_dirs']}\n"
            output += f"  - Total Size: {stats['total_size_bytes']:,} bytes\n\n"
            
            if languages:
                output += f"Programming Languages Detected:\n"
                for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                    output += f"  - {lang}: {count} files\n"
                output += "\n"
            
            if key_files:
                output += f"Key Configuration Files Found:\n"
                for filename in key_files.keys():
                    output += f"  - {filename}\n"
                output += "\n"
            
            output += f"Directory Structure (top 3 levels):\n"
            output += "-" * 50 + "\n"
            structure_preview = structure[:60]
            output += "\n".join(structure_preview)
            if len(structure) > 60:
                output += f"\n... and {len(structure) - 60} more items\n"
            
            return output
            
        except Exception as e:
            return f"Error analyzing repository structure: {str(e)}"
    
    def detect_components(self, repo_url: str) -> str:
        """Detect major components and functionalities in the repository.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            String describing detected components
        """
        clone_path = self.get_clone_path(repo_url)
        if not clone_path:
            return "Error: Repository not cloned. Please clone it first using clone_repo tool."
        
        try:
            components = []
            
            # Check for common directory patterns
            common_dirs = {
                'src': 'Source code directory',
                'lib': 'Library code',
                'app': 'Application code',
                'api': 'API implementation',
                'models': 'Data models',
                'views': 'View layer',
                'controllers': 'Controller layer',
                'services': 'Service layer',
                'utils': 'Utility functions',
                'helpers': 'Helper functions',
                'components': 'UI Components',
                'pages': 'Page components',
                'routes': 'Routing logic',
                'middleware': 'Middleware',
                'config': 'Configuration',
                'tests': 'Test suite',
                'docs': 'Documentation',
                'scripts': 'Utility scripts',
                'database': 'Database related',
                'migrations': 'Database migrations',
                'public': 'Public assets',
                'static': 'Static files',
                'templates': 'Template files',
                'agent': 'Agent implementation',
                'agents': 'Multiple agents',
                'tools': 'Tool implementations',
                'prompts': 'Prompt templates',
            }
            
            for dir_name, description in common_dirs.items():
                dir_path = clone_path / dir_name
                if dir_path.exists() and dir_path.is_dir():
                    # Count files in directory
                    file_count = sum(1 for _ in dir_path.rglob('*') if _.is_file())
                    components.append({
                        'name': dir_name,
                        'description': description,
                        'path': str(dir_path.relative_to(clone_path)),
                        'file_count': file_count
                    })
            
            # Check for framework-specific patterns
            frameworks = self._detect_frameworks(clone_path)
            
            # Format output
            output = f"Component Detection Analysis\n"
            output += f"=" * 50 + "\n\n"
            
            if frameworks:
                output += f"Detected Frameworks/Technologies:\n"
                for framework in frameworks:
                    output += f"  - {framework}\n"
                output += "\n"
            
            if components:
                output += f"Detected Components ({len(components)} found):\n"
                output += "-" * 50 + "\n"
                for i, comp in enumerate(components, 1):
                    output += f"\n{i}. {comp['name'].upper()}/\n"
                    output += f"   Description: {comp['description']}\n"
                    output += f"   Path: {comp['path']}\n"
                    output += f"   Files: {comp['file_count']}\n"
            else:
                output += "No standard component structure detected.\n"
                output += "This might be a simple project or use a custom structure.\n"
            
            return output
            
        except Exception as e:
            return f"Error detecting components: {str(e)}"
    
    def read_file(self, repo_url: str, file_path: str) -> str:
        """Read a specific file from the cloned repository.
        
        Args:
            repo_url: GitHub repository URL
            file_path: Relative path to file within repository
            
        Returns:
            File contents or error message
        """
        clone_path = self.get_clone_path(repo_url)
        if not clone_path:
            return "Error: Repository not cloned. Please clone it first using clone_repo tool."
        
        try:
            full_path = clone_path / file_path
            if not full_path.exists():
                return f"Error: File not found: {file_path}"
            
            if not full_path.is_file():
                return f"Error: Path is not a file: {file_path}"
            
            content = full_path.read_text(encoding='utf-8', errors='ignore')
            
            # Add header with file info
            output = f"File: {file_path}\n"
            output += f"Size: {len(content)} characters\n"
            output += f"Lines: {len(content.splitlines())}\n"
            output += "=" * 50 + "\n\n"
            output += content
            
            return output
            
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def extract_code_snippets(self, repo_url: str, component_path: str, file_extensions: Optional[List[str]] = None) -> str:
        """Extract code snippets from a specific component/directory.
        
        Args:
            repo_url: GitHub repository URL
            component_path: Relative path to component directory
            file_extensions: Optional list of file extensions to include (e.g., ['.py', '.js'])
            
        Returns:
            Code snippets with context
        """
        clone_path = self.get_clone_path(repo_url)
        if not clone_path:
            return "Error: Repository not cloned. Please clone it first using clone_repo tool."
        
        try:
            component_full_path = clone_path / component_path
            if not component_full_path.exists():
                return f"Error: Component path not found: {component_path}"
            
            snippets = []
            
            # Get all files in component
            if component_full_path.is_file():
                files = [component_full_path]
            else:
                files = list(component_full_path.rglob('*'))
                files = [f for f in files if f.is_file()]
            
            # Filter by extensions if provided
            if file_extensions:
                files = [f for f in files if f.suffix in file_extensions]
            
            # Limit to first 10 files to avoid overwhelming output
            files = files[:10]
            
            for file_path in files:
                try:
                    rel_path = file_path.relative_to(clone_path)
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    # Extract key parts (classes, functions, etc.)
                    key_parts = self._extract_key_code_parts(content, file_path.suffix)
                    
                    snippet_info = {
                        'file': str(rel_path),
                        'size': len(content),
                        'lines': len(content.splitlines()),
                        'preview': content[:500] if len(content) > 500 else content,
                        'key_parts': key_parts
                    }
                    snippets.append(snippet_info)
                    
                except Exception:
                    continue
            
            # Format output
            output = f"Code Snippets from: {component_path}\n"
            output += f"=" * 50 + "\n\n"
            output += f"Found {len(snippets)} files\n\n"
            
            for i, snippet in enumerate(snippets, 1):
                output += f"\n{i}. {snippet['file']}\n"
                output += f"   Size: {snippet['size']} chars, {snippet['lines']} lines\n"
                
                if snippet['key_parts']:
                    output += f"   Key elements: {', '.join(snippet['key_parts'][:5])}\n"
                
                output += f"\n   Preview:\n"
                output += "   " + "-" * 45 + "\n"
                for line in snippet['preview'].splitlines()[:15]:
                    output += f"   {line}\n"
                if snippet['lines'] > 15:
                    output += f"   ... ({snippet['lines'] - 15} more lines)\n"
                output += "\n"
            
            return output
            
        except Exception as e:
            return f"Error extracting code snippets: {str(e)}"
    
    # Helper methods
    
    def _get_repo_stats(self, path: Path) -> Dict[str, int]:
        """Get basic repository statistics."""
        stats = {'total_files': 0, 'total_dirs': 0, 'total_size_bytes': 0}
        try:
            for item in path.rglob('*'):
                if '.git' in item.parts:
                    continue
                if item.is_file():
                    stats['total_files'] += 1
                    try:
                        stats['total_size_bytes'] += item.stat().st_size
                    except:
                        pass
                elif item.is_dir():
                    stats['total_dirs'] += 1
        except:
            pass
        return stats
    
    def _get_directory_structure(self, path: Path, max_depth: int = 3, current_depth: int = 0) -> List[str]:
        """Get directory structure up to max_depth."""
        structure = []
        if current_depth >= max_depth:
            return structure
        
        try:
            for item in sorted(path.iterdir()):
                if item.name == '.git':
                    continue
                
                indent = "  " * current_depth
                if item.is_dir():
                    structure.append(f"{indent}{item.name}/")
                    sub_structure = self._get_directory_structure(item, max_depth, current_depth + 1)
                    structure.extend(sub_structure)
                else:
                    structure.append(f"{indent}{item.name}")
        except:
            pass
        
        return structure
    
    def _read_key_files(self, path: Path) -> Dict[str, str]:
        """Read important configuration files."""
        key_files = {}
        important_files = [
            'README.md', 'README.rst', 'README.txt', 'README',
            'package.json', 'requirements.txt', 'pyproject.toml',
            'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle',
            'setup.py', 'Makefile', 'Dockerfile', 'docker-compose.yml'
        ]
        
        for filename in important_files:
            file_path = path / filename
            if file_path.exists() and file_path.is_file():
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if len(content) > 3000:
                        content = content[:3000] + '\n... (truncated)'
                    key_files[filename] = content
                except:
                    pass
        
        return key_files
    
    def _detect_languages(self, path: Path) -> Dict[str, int]:
        """Detect programming languages by file extensions."""
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.cpp': 'C++',
            '.c': 'C',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.cs': 'C#',
            '.html': 'HTML',
            '.css': 'CSS',
            '.jsx': 'React JSX',
            '.tsx': 'React TSX',
            '.vue': 'Vue',
        }
        
        languages = {}
        try:
            for item in path.rglob('*'):
                if '.git' in item.parts or not item.is_file():
                    continue
                
                ext = item.suffix.lower()
                if ext in lang_map:
                    lang = lang_map[ext]
                    languages[lang] = languages.get(lang, 0) + 1
        except:
            pass
        
        return languages
    
    def _detect_frameworks(self, path: Path) -> List[str]:
        """Detect frameworks based on configuration files and structure."""
        frameworks = []
        
        # Check for specific files
        framework_indicators = {
            'package.json': ['Node.js/npm'],
            'requirements.txt': ['Python'],
            'pyproject.toml': ['Python (Poetry/Modern)'],
            'Cargo.toml': ['Rust'],
            'go.mod': ['Go'],
            'pom.xml': ['Java (Maven)'],
            'build.gradle': ['Java (Gradle)'],
            'Gemfile': ['Ruby'],
            'composer.json': ['PHP (Composer)'],
        }
        
        for file, fw_list in framework_indicators.items():
            if (path / file).exists():
                frameworks.extend(fw_list)
        
        # Check package.json for specific frameworks
        package_json = path / 'package.json'
        if package_json.exists():
            try:
                import json
                content = json.loads(package_json.read_text())
                deps = {**content.get('dependencies', {}), **content.get('devDependencies', {})}
                
                if 'react' in deps:
                    frameworks.append('React')
                if 'vue' in deps:
                    frameworks.append('Vue.js')
                if 'next' in deps:
                    frameworks.append('Next.js')
                if 'express' in deps:
                    frameworks.append('Express.js')
                if 'angular' in deps or '@angular/core' in deps:
                    frameworks.append('Angular')
            except:
                pass
        
        return frameworks
    
    def _extract_key_code_parts(self, content: str, file_ext: str) -> List[str]:
        """Extract key code parts like class names, function names."""
        key_parts = []
        
        try:
            lines = content.splitlines()
            
            if file_ext == '.py':
                for line in lines:
                    line = line.strip()
                    if line.startswith('class '):
                        class_name = line.split('(')[0].replace('class ', '').strip(':')
                        key_parts.append(f'class {class_name}')
                    elif line.startswith('def '):
                        func_name = line.split('(')[0].replace('def ', '')
                        key_parts.append(f'def {func_name}()')
            
            elif file_ext in ['.js', '.ts', '.jsx', '.tsx']:
                for line in lines:
                    line = line.strip()
                    if line.startswith('class '):
                        class_name = line.split('{')[0].replace('class ', '').strip()
                        key_parts.append(f'class {class_name}')
                    elif 'function ' in line:
                        func_name = line.split('(')[0].split('function ')[-1].strip()
                        key_parts.append(f'function {func_name}()')
                    elif line.startswith('const ') and '=>' in line:
                        const_name = line.split('=')[0].replace('const ', '').strip()
                        key_parts.append(f'const {const_name}')
        except:
            pass
        
        return key_parts
