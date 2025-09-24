"""
EagleView API Client - All Demos Runner
This script runs all demo files to showcase the complete functionality.
"""
import subprocess
import sys
from datetime import datetime

def run_demo(demo_name, file_path):
    """Run a demo and capture its output"""
    print("\n" + "="*80)
    print("RUNNING: {}".format(demo_name))
    print("FILE: {}".format(file_path))
    print("STARTED: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("="*80)
    
    try:
        result = subprocess.run([sys.executable, file_path], 
                              capture_output=True, text=True, timeout=60)
        
        if result.stdout:
            print("OUTPUT:")
            print(result.stdout)
        
        if result.stderr:
            print("ERRORS:")
            print(result.stderr)
            
        print("Return Code: {}".format(result.returncode))
        print("FINISHED: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("ERROR: Demo timed out after 60 seconds")
        return False
    except Exception as e:
        print("ERROR: Failed to run demo - {}".format(e))
        return False

def main():
    print("EAGLEVIEW API CLIENT - ALL DEMOS RUNNER")
    print("=" * 80)
    print("Starting all demos at: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("\nThis script will run all demo files to showcase the complete functionality.")
    
    demos = [
        ("Comprehensive Overview Demo", "demo_comprehensive.py"),
        ("CLI Functionality Demo", "demo_all_functionalities.py"), 
        ("Programmatic Usage Demo", "demo_programmatic_usage.py")
    ]
    
    results = []
    
    for demo_name, file_path in demos:
        success = run_demo(demo_name, file_path)
        results.append((demo_name, success))
    
    print("\n" + "="*80)
    print("DEMO EXECUTION SUMMARY")
    print("="*80)
    
    all_success = True
    for demo_name, success in results:
        status = "SUCCESS" if success else "FAILED"
        print("{:>8}: {}".format(status, demo_name))
        if not success:
            all_success = False
    
    print("\nOverall Result: {}".format('ALL DEMOS PASSED' if all_success else 'SOME DEMOS FAILED'))
    print("Completed at: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    if all_success:
        print("\nSUCCESS: All demos completed successfully!")
        print("\nThe EagleView API Client is properly configured and all functionality is working.")
        print("You can now use any of the demo files to explore specific aspects of the system.")
    else:
        print("\nWARNING: Some demos encountered issues.")
        print("Please check the output above for details and ensure all dependencies are installed.")

if __name__ == "__main__":
    main()