#!/usr/bin/env python3
"""
Environment Setup Test Script
AI Networking Workshop

Run this script to verify your environment is ready for the workshop.
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} (need 3.10+)")
        return False

def check_ollama():
    """Check if Ollama is installed and running"""
    print("\nChecking Ollama...")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("  ✅ Ollama is installed")
            if 'llama3.2' in result.stdout:
                print("  ✅ llama3.2:3b model found")
            else:
                print("  ⚠️  llama3.2:3b model not found")
                print("     Run: ollama pull llama3.2:3b")
            return True
        else:
            print("  ❌ Ollama not responding")
            return False
    except FileNotFoundError:
        print("  ❌ Ollama not installed")
        print("     Install from: https://ollama.com/")
        return False
    except Exception as e:
        print(f"  ❌ Error checking Ollama: {e}")
        return False

def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is not None:
        print(f"  ✅ {package_name}")
        return True
    else:
        print(f"  ❌ {package_name} not installed")
        return False

def check_python_packages():
    """Check required Python packages"""
    print("\nChecking Python packages...")
    packages = [
        ('requests', 'requests'),
        ('anthropic', 'anthropic'),
    ]
    
    all_installed = True
    for pkg_name, import_name in packages:
        if not check_package(pkg_name, import_name):
            all_installed = False
    
    if not all_installed:
        print("\n  Install missing packages:")
        print("  pip install -r requirements.txt")
    
    return all_installed

def check_api_key():
    """Check if Anthropic API key is set"""
    print("\nChecking API key...")
    import os
    if os.getenv('ANTHROPIC_API_KEY'):
        print("  ✅ ANTHROPIC_API_KEY is set")
        return True
    else:
        print("  ⚠️  ANTHROPIC_API_KEY not set (optional for Labs 1-2)")
        print("     Required for Labs 3-4")
        print("     Set with: export ANTHROPIC_API_KEY=your-key-here")
        return False

def test_mock_devices():
    """Test mock network devices"""
    print("\nTesting mock network devices...")
    try:
        # Try to import from examples directory
        sys.path.insert(0, 'examples')
        from mock_network_devices import get_device_status
        
        result = get_device_status('spine1')
        if result.get('status') == 'up':
            print("  ✅ Mock devices working")
            return True
        else:
            print("  ❌ Mock devices returned unexpected result")
            return False
    except ImportError:
        print("  ❌ Cannot import mock_network_devices")
        print("     Make sure you're in the workshop directory")
        return False
    except Exception as e:
        print(f"  ❌ Error testing mock devices: {e}")
        return False

def main():
    """Run all checks"""
    print("="*70)
    print("AI Networking Workshop - Environment Test")
    print("="*70)
    
    checks = [
        check_python_version(),
        check_ollama(),
        check_python_packages(),
        check_api_key(),
        test_mock_devices()
    ]
    
    print("\n" + "="*70)
    print("Summary:")
    print("="*70)
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ All checks passed ({passed}/{total})")
        print("\nYou're ready for the workshop! 🎉")
    elif passed >= 3:
        print(f"⚠️  Most checks passed ({passed}/{total})")
        print("\nYou can start the workshop, but some labs may not work")
    else:
        print(f"❌ Several checks failed ({passed}/{total})")
        print("\nPlease fix the issues above before starting")
    
    print("="*70)

if __name__ == "__main__":
    main()
