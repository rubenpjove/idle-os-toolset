import argparse
from google import genai
from google.genai import types
import os
import json
import subprocess
import shlex

home=os.path.expanduser("~")
os_info_path=home+"/data/virtual_machines/os_info/"
client = genai.Client()
model = "gemini-flash-latest"


def generate_commands(vagrant_box, vm_name):
    content = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=f"""
            I am utilizing the following Vagrant box: https://portal.cloud.hashicorp.com/vagrant/discover/{vagrant_box}. 
            
            Provide the necessary commands to obtain the OS information. The commands should return the output in the terminal. The OS information should include details such as OS family, OS type, and OS version.
            
            OUTPUT FORMAT:
            You must respond ONLY with a valid JSON object. Do not include explanations or markdown backticks.
            The JSON structure must be:
            {{
            "Commands": ["command1", "command2"]
            }}
            """
            ),
        ],
    )
    tools = [
        types.Tool(url_context=types.UrlContext()),
    ]
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
    )
    response = client.models.generate_content(
            model=model,
            contents=content,
            config=generate_content_config,
    )

    content = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=f"""
            I have generated the following commands to obtain OS information for the Vagrant box: {vagrant_box}. The commands are: {response.text}.
            Please return the commands in a JSON format with the following structure:
            {{
            "Commands": ["command1", "command2"]
            }}
                        """
                        ),
                    ],
            )
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
            response_schema=genai.types.Schema(
                type = genai.types.Type.OBJECT,
                required = ["Commands"],
                properties = {
                    "Commands": genai.types.Schema(
                        type = genai.types.Type.ARRAY,
                        items = genai.types.Schema(
                            type = genai.types.Type.STRING,
                        ),
                    ),
                },
            ),
    )
    response = client.models.generate_content(
            model=model,
            contents=content,
            config=generate_content_config,
    )

    os.makedirs(os_info_path + vm_name, exist_ok=True)
    with open(os_info_path + vm_name + "/commands.json", "w") as f:
        try:
            json_data = json.loads(response.text)
            json.dump(json_data, f, indent=4)
        except json.JSONDecodeError:
            f.write(response.text)

def execute_commands(vagrant_box, vm_name):

    with open(os_info_path + vm_name + "/commands.json", "r") as f:
        data = json.load(f)
        commands = data.get("Commands", [])
        command_outputs = {}
        print(f"Executing commands for {vm_name}:")
        if "windows" in vm_name.lower():
            remote_command = "vagrant winrm -c '{}'"
        else:
            remote_command = "vagrant ssh -c '{}'"
        for command in commands:
            try:
                command_to_run = shlex.split(remote_command.format(command))
                result = subprocess.run(command_to_run, capture_output=True, text=True)
                command_outputs[command] = result.stdout

            except Exception as e:
                print(f"Error executing command '{command}': {e}")

    with open(os_info_path + vm_name + "/commands_execute.json", "w") as f:
        json.dump(command_outputs, f, indent=4)


def get_os_info(vagrant_box, vm_name):
    with open(os_info_path + vm_name + "/commands_execute.json", "r") as f:
        command_outputs = json.load(f)
    contents = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=f"""
            I have executed the following commands using the Vagrant box: {vagrant_box} and obtained the following outputs: {json.dumps(command_outputs)}.
            Analyze the command outputs and provide a summary of the OS information. You must respond with the Os_Family, Os_Type and Os_Version."""
            ),
        ],
    )

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["Os_Family", "Os_Type", "Os_Version"],
            properties = {
                "Os_Family": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "Os_Type": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "Os_Version": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        ),
    )
    response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
    )

    with open(os_info_path + vm_name + "/os_info.json", "w") as f:
        try:
            json_data = json.loads(response.text)
            json.dump(json_data, f, indent=4)
        except json.JSONDecodeError:
            f.write(response.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get OS information of a vagrant box."
    )
    parser.add_argument(
        "-v", "--vagrant_box",
        type=str,
        help="Vagrant box name (example: datacastle/windows7)",
    )
    parser.add_argument(
        "-b", "--vm_name",
        type=str,
        help="Virtual machine name (example: windows_windows7)",
    )

    args = parser.parse_args()

    print(f"Getting OS info commands for virtual machine: {args.vm_name} with Vagrant box: {args.vagrant_box}")
    generate_commands(args.vagrant_box,args.vm_name)
    print(f"Commands saved to {os_info_path + args.vm_name + '/commands.json'}")
    execute_commands(args.vagrant_box,args.vm_name)
    print(f"Command outputs saved to {os_info_path + args.vm_name + '/commands_execute.json'}")
    get_os_info(args.vagrant_box,args.vm_name)
    print(f"OS information saved to {os_info_path + args.vm_name + '/os_info.json'}")



