def read_file(path):
    with open(path) as f:
        return f.read().strip().lower()

pr_type = read_file("pr_type.txt")
tests_present = read_file("tests_present.txt") == "true"

print(f"PR type: {pr_type}")
print(f"Tests present: {tests_present}")

action = "skip"

if pr_type == "bug" and not tests_present:
    action = "generate_regression_tests"
elif pr_type == "feature" and not tests_present:
    action = "generate_feature_tests"

print(f"🧪 Test generation action: {action}")

with open("test_action.txt", "w") as f:
    f.write(action)

if action == "skip":
    print("🛑 Skipping test generation")
    exit(0)

print(f"🚀 Generating tests: {action}")