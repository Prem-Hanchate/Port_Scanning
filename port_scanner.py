#!/usr/bin/env python3
"""
Advanced Port Scanner - Python Controller & Brain
Handles user input, automation, and report formatting
Calls Bash script for heavy Nmap scanning operations
"""

import subprocess
import sys
import os
from datetime import datetime
import platform


class PortScanner:
    """Main controller class for the hybrid port scanning tool"""
    
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.bash_script = os.path.join(self.script_dir, "advanced_port_scan.sh")
        self.temp_output = "scan_temp_output.txt"
        
    def print_banner(self):
        """Display tool banner"""
        banner = """
╔══════════════════════════════════════════════════════╗
║     ADVANCED PORT SCANNING TOOL                      ║
║     Python + Bash Hybrid Scanner                     ║
╚══════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def validate_input(self, target, ports):
        """Basic validation of user input"""
        if not target:
            print("❌ Error: Target cannot be empty")
            return False
        if not ports:
            print("❌ Error: Port range cannot be empty")
            return False
        return True
        
    def get_user_input(self):
        """Collect scanning parameters from user"""
        print("\n📋 Configuration")
        print("-" * 54)
        
        target = input("Enter Target (IP/Domain/Network): ").strip()
        if not target:
            target = "127.0.0.1"
            print(f"   Using default: {target}")
            
        ports = input("Enter Port Range (e.g., 1-1024, 80,443): ").strip()
        if not ports:
            ports = "1-1024"
            print(f"   Using default: {ports}")
            
        return target, ports
        
    def check_requirements(self):
        """Check if required tools are available"""
        print("\n🔍 Checking Requirements...")
        
        # Check if nmap is installed
        try:
            result = subprocess.run(
                ["nmap", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("   ✓ Nmap is installed")
            else:
                print("   ✗ Nmap is not installed properly")
                return False
        except FileNotFoundError:
            print("   ✗ Nmap is not installed")
            print("   💡 Install: sudo apt-get install nmap (Linux) or brew install nmap (Mac)")
            return False
        except Exception as e:
            print(f"   ⚠ Warning: Could not verify Nmap: {e}")
            
        # Check if bash script exists
        if not os.path.exists(self.bash_script):
            print(f"   ✗ Bash script not found: {self.bash_script}")
            return False
        print(f"   ✓ Bash script found")
        
        return True
        
    def run_bash_scanner(self, target, ports):
        """Execute the Bash scanning script using subprocess"""
        print("\n⚡ Starting Scan Process...")
        print("-" * 54)
        
        try:
            # Determine shell command based on OS
            if platform.system() == "Windows":
                # Windows: Use WSL or Git Bash
                # Try WSL first
                try:
                    cmd = ["wsl", "bash", self.bash_script, target, ports, self.temp_output]
                    print("   🐧 Using WSL (Windows Subsystem for Linux)")
                except FileNotFoundError:
                    # Fallback to Git Bash
                    cmd = ["bash", self.bash_script, target, ports, self.temp_output]
                    print("   🔧 Using Git Bash")
            else:
                # Linux/Mac
                cmd = ["bash", self.bash_script, target, ports, self.temp_output]
                print("   🐧 Using Bash")
                
            # Run the bash script
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Print stderr output (progress messages from bash)
            if result.stderr:
                print(result.stderr)
                
            if result.returncode != 0:
                print(f"❌ Error: Bash script failed with return code {result.returncode}")
                if result.stdout:
                    print("Output:", result.stdout)
                return False
                
            print("✅ Scan completed successfully")
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Error: Scan timeout (exceeded 5 minutes)")
            return False
        except FileNotFoundError:
            print("❌ Error: Bash not found. Make sure Bash is installed.")
            print("   💡 Windows users: Install WSL or Git Bash")
            return False
        except Exception as e:
            print(f"❌ Error running scan: {e}")
            return False
            
    def process_and_format_report(self, target):
        """Read raw scan output and create formatted final report"""
        print("\n📝 Processing Report...")
        
        try:
            # Read the temporary output file
            if not os.path.exists(self.temp_output):
                print(f"❌ Error: Temporary output file not found: {self.temp_output}")
                return None
                
            with open(self.temp_output, 'r', encoding='utf-8', errors='ignore') as f:
                raw_data = f.read()
                
            # Generate final report filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_report = f"port_scan_report_{target.replace('/', '_')}_{timestamp}.txt"
            
            # Create enhanced report
            with open(final_report, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("         PROFESSIONAL PORT SCANNING REPORT\n")
                f.write("         Python + Bash Hybrid Tool\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Generated by: Port Scanner v1.0\n")
                f.write(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Platform: {platform.system()} {platform.release()}\n")
                f.write("\n" + "=" * 70 + "\n\n")
                f.write(raw_data)
                f.write("\n" + "=" * 70 + "\n")
                f.write("         END OF REPORT\n")
                f.write("=" * 70 + "\n")
                
            print(f"   ✓ Final report created: {final_report}")
            
            # Clean up temporary file
            try:
                os.remove(self.temp_output)
                print(f"   ✓ Temporary files cleaned up")
            except Exception as e:
                print(f"   ⚠ Warning: Could not remove temp file: {e}")
                
            return final_report
            
        except Exception as e:
            print(f"❌ Error processing report: {e}")
            return None
            
    def display_summary(self, report_file):
        """Display scan summary and next steps"""
        print("\n" + "=" * 54)
        print("🎉 SCAN COMPLETED SUCCESSFULLY")
        print("=" * 54)
        print(f"\n📄 Report saved as: {report_file}")
        print(f"📂 Location: {os.path.abspath(report_file)}")
        print("\n💡 Next Steps:")
        print("   • Review the report for open ports and services")
        print("   • Verify expected services are running")
        print("   • Check for unexpected open ports")
        print("   • Update firewall rules if needed")
        print("\n" + "=" * 54)
        
    def run(self):
        """Main execution flow"""
        self.print_banner()
        
        # Step 1: Check requirements
        if not self.check_requirements():
            print("\n❌ Requirements check failed. Please install missing components.")
            return 1
            
        # Step 2: Get user input
        target, ports = self.get_user_input()
        
        if not self.validate_input(target, ports):
            return 1
            
        # Step 3: Run bash scanner
        if not self.run_bash_scanner(target, ports):
            print("\n❌ Scanning failed. Check the errors above.")
            return 1
            
        # Step 4: Process and format report
        report_file = self.process_and_format_report(target)
        if not report_file:
            print("\n❌ Report generation failed.")
            return 1
            
        # Step 5: Display summary
        self.display_summary(report_file)
        
        return 0


def main():
    """Entry point"""
    try:
        scanner = PortScanner()
        exit_code = scanner.run()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
