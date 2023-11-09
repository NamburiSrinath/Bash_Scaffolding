from transformers import T5ForConditionalGeneration, T5Tokenizer
import subprocess
import platform
import psutil
import torch

# Load the T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")

# Define a function to run Bash commands
def run_bash_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

# Define a function to answer system-related questions
def answer_system_question(question):
    system = platform.system()

    if "ip address" in question.lower():
        if system == "Linux":
            command = "hostname -I | awk '{print $1}'"
        elif system == "Windows":
            command = "ipconfig | findstr IPv4"
        else:
            return "Sorry, I don't know how to find the IP address on this platform."

        ip_address = run_bash_command(command)
        return ip_address

    elif "ram" in question.lower():
        ram = psutil.virtual_memory()
        return f"Available RAM: {ram.available / (1024 ** 3):.2f} GB"

    elif "gpu status" in question.lower():
        if system == "Linux":
            command = "nvidia-smi"
            gpu_status = run_bash_command(command)
            return gpu_status
        else:
            return "GPU status is not available on this platform."

    return "I'm not sure how to answer that question."

# Define a function to answer questions about PIDs
def answer_pid_question(question):
    process_name = question.lower().replace("what's the pid of", "").strip()
    pids = [str(p.info['pid']) for p in psutil.process_iter(attrs=["name", "pid"]) if process_name in p.info['name'].lower()]
    if pids:
        users = [run_bash_command(f"ps -u -p {pid}").strip() for pid in pids]
        pid_info = [f"PID: {pid}, User: {user}" for pid, user in zip(pids, users)]
        return f"{process_name} PIDs and Users:\n" + "\n".join(pid_info)
    else:
        return f"No process found with the name: {process_name}"

# Define a function to generate a response using the T5 model
def generate_response(prompt):
    input_text = "bash: " + prompt if prompt.startswith("!") else "chat: " + prompt
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    with torch.no_grad():
        response_ids = model.generate(input_ids)

    response_text = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response_text

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        if user_input.lower().startswith("what's the"):
            if " PID of" in user_input:
                # Answer PID-related questions
                response = answer_pid_question(user_input)
            else:
                # Answer system-related questions
                response = answer_system_question(user_input)
        else:
            # Use the T5 model for other queries
            response = generate_response(user_input)

        print("Model:", response)

        if user_input.startswith("!"):
            # Execute Bash command
            command = user_input[1:]
            result = run_bash_command(command)
            print(result)
