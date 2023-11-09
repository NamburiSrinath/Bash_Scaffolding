# Bash_Scaffolding

I've implemented a basic version of bash scaffolding
- Model used is Flan-T5-Large (780M)
- If it's a casual question, I will output the model's response 
- If the question has specific keywords, then the code redirects to specific functions such as
1. Getting RAM
2. Getting IP address
3. GPU usage
4. PID of a particular process
- If you want to execute another code from this command, can start with !. For example, !python code_testing.py will execute the other code and returns to user-input!
- If I enter exit, the termination stops

Most of it is possible via psutils, subprocess libraries and as you suggested, has the subcommand.run() for each model input!
