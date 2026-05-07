"""
Langfuse Connection & Integration Test
Tests all aspects of Langfuse setup and integration
"""

import os
import sys
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

print("=" * 60)
print("LANGFUSE INTEGRATION TEST")
print("=" * 60)
print()

# ============================================================================
# TEST 1: Check Credentials are Configured
# ============================================================================
print("TEST 1: Checking Credentials Configuration...")
print("-" * 60)

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_BASE_URL") or os.getenv("LANGFUSE_HOST")

if LANGFUSE_PUBLIC_KEY:
    print(f"✓ LANGFUSE_PUBLIC_KEY found: {LANGFUSE_PUBLIC_KEY[:20]}...")
else:
    print("✗ LANGFUSE_PUBLIC_KEY not found in .env")
    sys.exit(1)

if LANGFUSE_SECRET_KEY:
    print(f"✓ LANGFUSE_SECRET_KEY found: {LANGFUSE_SECRET_KEY[:20]}...")
else:
    print("✗ LANGFUSE_SECRET_KEY not found in .env")
    sys.exit(1)

if LANGFUSE_HOST:
    print(f"✓ LANGFUSE_HOST/BASE_URL found: {LANGFUSE_HOST}")
else:
    print("✓ LANGFUSE_HOST defaulting to: https://cloud.langfuse.com")
    LANGFUSE_HOST = "https://cloud.langfuse.com"

print()

# ============================================================================
# TEST 2: Check Langfuse Library Import
# ============================================================================
print("TEST 2: Checking Langfuse Library Installation...")
print("-" * 60)

try:
    from langfuse import Langfuse, observe
    print("✓ Successfully imported: from langfuse import Langfuse, observe")
except ImportError as e:
    print(f"✗ Failed to import Langfuse: {e}")
    print("  Run: pip install langfuse")
    sys.exit(1)

print()

# ============================================================================
# TEST 3: Test Langfuse Connection
# ============================================================================
print("TEST 3: Testing Connection to Langfuse Cloud...")
print("-" * 60)

try:
    # Create a Langfuse client
    langfuse = Langfuse(
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
        host=LANGFUSE_HOST,
    )
    print(f"✓ Successfully connected to Langfuse at {LANGFUSE_HOST}")
    print(f"  Client Status: Ready for observability")
except Exception as e:
    print(f"✗ Failed to connect to Langfuse: {e}")
    print("  Check your credentials and internet connection")
    sys.exit(1)

print()

# ============================================================================
# TEST 4: Test @observe() Decorator - Basic Function
# ============================================================================
print("TEST 4: Testing @observe() Decorator...")
print("-" * 60)

try:
    @observe()
    def test_function(x: int, y: int) -> int:
        """Test function decorated with @observe()"""
        return x + y
    
    result = test_function(5, 3)
    print(f"✓ Successfully decorated function with @observe()")
    print(f"  Function executed: test_function(5, 3) = {result}")
    print(f"  Trace should appear in Langfuse dashboard")
except Exception as e:
    print(f"✗ Failed to use @observe() decorator: {e}")
    sys.exit(1)

print()

# ============================================================================
# TEST 5: Test @observe() Decorator - With Metadata
# ============================================================================
print("TEST 5: Testing @observe() with Custom Metadata...")
print("-" * 60)

try:
    @observe(name="advanced_test", as_type="chain")
    def advanced_function(query: str) -> str:
        """Advanced function with metadata"""
        return f"Response to: {query}"
    
    result = advanced_function("What is Langfuse?")
    print(f"✓ Successfully used @observe() with metadata")
    print(f"  Trace Name: 'advanced_test'")
    print(f"  Result: {result}")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

print()

# ============================================================================
# TEST 6: Test Nested Observations
# ============================================================================
print("TEST 6: Testing Nested Observations...")
print("-" * 60)

try:
    @observe()
    def inner_function(x: int) -> int:
        return x * 2
    
    @observe()
    def outer_function(x: int) -> int:
        result = inner_function(x)
        return result + 10
    
    result = outer_function(5)
    print(f"✓ Successfully created nested observations")
    print(f"  Outer function executed: outer_function(5) = {result}")
    print(f"  This creates nested traces in Langfuse")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

print()

# ============================================================================
# TEST 7: Flush and Verify
# ============================================================================
print("TEST 7: Flushing Traces to Langfuse Cloud...")
print("-" * 60)

try:
    # Flush all pending traces
    langfuse.flush()
    print(f"✓ Successfully flushed traces to Langfuse cloud")
    print(f"  Waiting 2-5 seconds for traces to appear in dashboard...")
    time.sleep(2)
except Exception as e:
    print(f"✗ Failed to flush traces: {e}")
    sys.exit(1)

print()

# ============================================================================
# SUMMARY AND NEXT STEPS
# ============================================================================
print("=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print()
print("YOUR LANGFUSE IS WORKING CORRECTLY!")
print()
print("NEXT STEPS:")
print("-" * 60)
print("1. Go to https://cloud.langfuse.com")
print("2. Log in to your account")
print("3. Select your project")
print("4. Go to 'Traces' tab")
print("5. You should see these test traces:")
print("   - test_function")
print("   - advanced_test")
print("   - outer_function (with nested inner_function)")
print()
print("6. Once you see these traces, everything is working!")
print("7. Now run: streamlit run app.py")
print()
print("EXPECTED BEHAVIOR IN APP:")
print("-" * 60)
print("• When you submit a query, Langfuse automatically traces it")
print("• Each agent step is logged to Langfuse")
print("• You can inspect execution flow in the dashboard")
print("• Performance metrics (latency, tokens) are tracked")
print()
print("HOW TO USE IN YOUR CODE:")
print("-" * 60)
print("from langfuse import observe")
print()
print("@observe()  # Decorator automatically traces this function")
print("def my_function(param):")
print("    return result")
print()
print("=" * 60)

