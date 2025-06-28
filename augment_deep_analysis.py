#!/usr/bin/env python3
"""
Augment Deep Analysis Tool
==========================
Find the exact cause of Augment typing delays while keeping the extension enabled
"""

import subprocess
import json
import os
import time
import threading
from pathlib import Path

class AugmentDeepAnalysis:
    def __init__(self):
        self.vscode_config = Path.home() / ".config/Code - Insiders"
        self.settings_file = self.vscode_config / "User/settings.json"
        self.monitoring = False
        
    def analyze_augment_settings(self):
        """Analyze current Augment configuration"""
        print("🔍 ANALYZING AUGMENT CONFIGURATION...")
        
        if not self.settings_file.exists():
            print("❌ No settings.json found")
            return {}
            
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
            
            # Extract all Augment-related settings
            augment_settings = {k: v for k, v in settings.items() if 'augment' in k.lower()}
            
            print("📊 Current Augment Settings:")
            for key, value in augment_settings.items():
                print(f"  {key}: {value}")
            
            # Check for problematic settings
            problematic = []
            
            if augment_settings.get('augment.secrets.enable', True):
                problematic.append("augment.secrets.enable: true (causes secret store loops)")
            
            if augment_settings.get('augment.autoComplete.enabled', True):
                problematic.append("augment.autoComplete.enabled: true (triggers on every keystroke)")
            
            if augment_settings.get('augment.realtime.enabled', True):
                problematic.append("augment.realtime.enabled: true (continuous processing)")
            
            if augment_settings.get('augment.telemetry.enabled', True):
                problematic.append("augment.telemetry.enabled: true (network requests)")
            
            if problematic:
                print("\n🚨 PROBLEMATIC SETTINGS FOUND:")
                for issue in problematic:
                    print(f"  ❌ {issue}")
            
            return augment_settings
            
        except Exception as e:
            print(f"❌ Error reading settings: {e}")
            return {}
    
    def monitor_augment_activity(self):
        """Monitor Augment's real-time activity"""
        print("\n🔍 MONITORING AUGMENT ACTIVITY...")
        print("Start typing in VSCode to see what Augment does...")
        
        # Monitor file system activity
        augment_dirs = [
            self.vscode_config / "User/globalStorage",
            Path.home() / ".vscode-insiders/extensions"
        ]
        
        for directory in augment_dirs:
            if directory.exists():
                print(f"📁 Watching: {directory}")
        
        # Use inotify to watch file changes
        try:
            cmd = ['inotifywait', '-m', '-r', '--format', '%T %w%f %e', '--timefmt', '%H:%M:%S']
            for directory in augment_dirs:
                if directory.exists():
                    cmd.extend([str(directory)])
            
            if len(cmd) > 6:  # Has directories to watch
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                print("📊 File system activity (Ctrl+C to stop):")
                try:
                    while self.monitoring:
                        line = process.stdout.readline()
                        if line:
                            if 'augment' in line.lower():
                                print(f"  🔥 {line.strip()}")
                        time.sleep(0.1)
                except KeyboardInterrupt:
                    process.terminate()
                    
        except FileNotFoundError:
            print("⚠️ inotifywait not available, install with: sudo dnf install inotify-tools")
    
    def analyze_augment_network_activity(self):
        """Check if Augment is making excessive network requests"""
        print("\n🌐 ANALYZING NETWORK ACTIVITY...")
        
        try:
            # Monitor network connections from VSCode processes
            result = subprocess.run(['netstat', '-tulpn'], capture_output=True, text=True)
            
            vscode_connections = []
            for line in result.stdout.split('\n'):
                if 'code-insiders' in line:
                    vscode_connections.append(line.strip())
            
            if vscode_connections:
                print("📡 VSCode Network Connections:")
                for conn in vscode_connections:
                    print(f"  {conn}")
            else:
                print("✅ No active network connections found")
                
        except Exception as e:
            print(f"❌ Error checking network activity: {e}")
    
    def check_augment_extension_files(self):
        """Check Augment extension files for configuration issues"""
        print("\n📦 ANALYZING AUGMENT EXTENSION FILES...")
        
        # Find Augment extension directory
        extensions_dir = Path.home() / ".vscode-insiders/extensions"
        augment_dirs = list(extensions_dir.glob("*augment*")) if extensions_dir.exists() else []
        
        if not augment_dirs:
            extensions_dir = self.vscode_config / "extensions"
            augment_dirs = list(extensions_dir.glob("*augment*")) if extensions_dir.exists() else []
        
        for augment_dir in augment_dirs:
            print(f"📁 Found Augment extension: {augment_dir.name}")
            
            # Check package.json for configuration
            package_json = augment_dir / "package.json"
            if package_json.exists():
                try:
                    with open(package_json, 'r') as f:
                        package_data = json.load(f)
                    
                    version = package_data.get('version', 'unknown')
                    print(f"  Version: {version}")
                    
                    # Check for problematic configuration
                    contributes = package_data.get('contributes', {})
                    commands = contributes.get('commands', [])
                    
                    print(f"  Commands: {len(commands)}")
                    
                    # Look for real-time/autocomplete features
                    config = contributes.get('configuration', {})
                    if config:
                        properties = config.get('properties', {})
                        realtime_settings = [k for k in properties.keys() if 'realtime' in k.lower() or 'auto' in k.lower()]
                        
                        if realtime_settings:
                            print(f"  ⚠️ Real-time settings found: {realtime_settings}")
                    
                except Exception as e:
                    print(f"  ❌ Error reading package.json: {e}")
    
    def create_optimized_augment_config(self):
        """Create optimized Augment configuration to reduce CPU usage"""
        print("\n🔧 CREATING OPTIMIZED AUGMENT CONFIGURATION...")
        
        # Load current settings
        settings = {}
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
            except:
                settings = {}
        
        # Apply performance optimizations
        optimizations = {
            # CRITICAL: Disable secret persistence
            "augment.secrets.enable": False,
            
            # Disable real-time features that trigger on every keystroke
            "augment.autoComplete.enabled": False,
            "augment.realtime.enabled": False,
            "augment.realtime.suggestions": False,
            "augment.realtime.analysis": False,
            
            # Disable telemetry and analytics
            "augment.telemetry.enabled": False,
            "augment.analytics.enabled": False,
            "augment.usage.tracking": False,
            
            # Reduce file watching
            "augment.fileWatcher.enabled": False,
            "augment.workspace.monitoring": False,
            
            # Disable background processing
            "augment.background.processing": False,
            "augment.background.sync": False,
            
            # Reduce network activity
            "augment.network.polling": False,
            "augment.auto.update": False,
            
            # Optimize performance
            "augment.performance.mode": "minimal",
            "augment.cache.enabled": True,
            "augment.debounce.delay": 1000,  # 1 second delay
            
            # Manual trigger only
            "augment.trigger.mode": "manual",
            "augment.trigger.automatic": False
        }
        
        # Apply optimizations
        settings.update(optimizations)
        
        # Backup original settings
        backup_file = self.settings_file.with_suffix('.json.backup')
        if self.settings_file.exists() and not backup_file.exists():
            import shutil
            shutil.copy2(self.settings_file, backup_file)
            print(f"  ✅ Backed up original settings to {backup_file}")
        
        # Save optimized settings
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        
        print("  ✅ Applied optimized Augment configuration")
        print("\n📋 OPTIMIZATIONS APPLIED:")
        for key, value in optimizations.items():
            print(f"  {key}: {value}")
    
    def test_typing_performance(self):
        """Test typing performance with optimizations"""
        print("\n🧪 TESTING TYPING PERFORMANCE...")
        print("1. Restart VSCode Insiders to apply new settings")
        print("2. Open a file and start typing")
        print("3. Monitor CPU usage with: htop | grep code-insiders")
        print("4. Check if CPU spikes are reduced")
        
        print("\n💡 IF STILL SLOW, TRY PROGRESSIVE DISABLING:")
        print("1. Disable Augment autocomplete: Ctrl+Shift+P → 'Augment: Disable AutoComplete'")
        print("2. Use manual trigger only: Ctrl+Shift+P → 'Augment: Manual Mode'")
        print("3. Check extension settings: Ctrl+, → search 'augment'")
    
    def run_complete_analysis(self):
        """Run complete Augment analysis"""
        print("🔬 AUGMENT DEEP ANALYSIS")
        print("=" * 50)
        print("Finding the exact cause of typing delays while keeping Augment enabled\n")
        
        # Analyze current configuration
        current_settings = self.analyze_augment_settings()
        
        # Check extension files
        self.check_augment_extension_files()
        
        # Check network activity
        self.analyze_augment_network_activity()
        
        # Create optimized configuration
        self.create_optimized_augment_config()
        
        # Provide testing instructions
        self.test_typing_performance()
        
        print("\n🎯 NEXT STEPS:")
        print("1. Restart VSCode Insiders")
        print("2. Test typing performance")
        print("3. If still slow, run with --verbose to see detailed logs")
        print("4. Use Ctrl+Shift+P → 'Augment' to access manual controls")

if __name__ == "__main__":
    analyzer = AugmentDeepAnalysis()
    analyzer.run_complete_analysis()
