
### Documentation

Ansible has surprisingly good [documentation](https://docs.ansible.com/ansible/latest/), use it find new modules and how to use a module.

They also have a [best practice](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html) that is good to read.



### How to run playbooks

First open `group_vars/all.yml` and replace the commented values so it suits you.

Use the command `ansible-playbook` to run playbooks.

To create instances use `ansible-playbook provision_instances.yml`.

To destroy instances use `ansible-playbook terminate_instances.yml`.



### Structure

#### Playbooks

We have 4 playbooks provision_instances, terminate_instances, gather__instances, site.

**provision_instances** is used to create 3 servers on Azure together with their respective security groups, network settings and storage.   
It Uses the roles provision_instances that waits for all of the security_groups to be created. It also connects the load balancers ip to your domain name.

**gather__instances** fins all active virtual machines has an ip address connected to it and, adds them to the hosts. After we have run this playbook we can use the following hosts in other playbooks: 
- `appServer` only the server for the app
- `database` only for the database server
- `loadBalancer` only the load balancer server

**terminate_instances** destroys virtual machines and assets connected to it. You can choose which ones to remove by changing the `instances` variable inside its `vars/main.yml` file.

**site** should run all of your playbooks to setup the whole project from scratch to a running production.



#### Other

**group_vars** contains variable files connected to hosts.

**roles** contains roles used by the playbooks.

**ansible.cfg** configuration for Ansible

**hosts** contains host groups. We only have the host `local` because our servers are dynamic and we used the playbook `gather_instances` instead.



### Credentials

#### ssh-keys
Without ssh-key files we need to enter the password for out ssh-key every time we run a task. To avoid this, make sure you have added your ssh-key to the ssh-agent. Do following commands or run `make add-ssh` in root folder (you need to replace <path-to-ssh-key> in `Makefile` to use this command).

```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/azure
```

#### Azure

You need credentials from Azure to allow Ansible to manage servers. 
This can be done by ether creating a file in your `$HOME/.azure/` folder called `credentials` or using ENV variables.

The `credentials` requires you to add the login information together with the subscription id.
The file should look like the following:

```
[default]
ad_user=<acronym>@student.bth.se
password=<password>
subscription_id=<XXxxxxXX-XxxX-XxxX-XxxX-XXxxxXXXxxXX>
tenant=<yyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy>
```

Replace `acronym` with your student acronym. The `password` should be the same you use to login in to azure. Your `subscription_id` can be found inside the *Information* box when overlooking your resource group on the website.

The environmental variables uses the same values but slightly different keys:

```
export AZURE_AD_USER='acronym@student.bth.se'
export AZURE_PASSWORD='<password>'
export AZURE_SUBSCRIPTION_ID='<XXxxxxXX-XxxX-XxxX-XxxX-XXxxxXXXxxXX>'
export AZURE_TENANT=`<yyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy>`
```

#### Ansible vault

We can use [ansible-vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) to encrypt files that contain sensitive information. Things that we want to push to GitHub while not having them visible, such as passwords.

Create a file with the following content, put it outside of the repo folder. Replace `<password>` with a password.

```
#!/bin/bash
cat <<EOF
<password>
EOF
```

Create a new ENV variable with the path to the password file, `ANSIBLE_VAULT_PASSWORD_FILE=<path-to-file>`.

Can now use `ansible-vault decrypt` and `ansible-vault encrypt` without typing password.

To create the decryption file on **CircleCI**, add an env variable and `echo` its value into a `.txt` file.

Example:
```yml
- run:
    name: Prepare the password file
    command: echo "$VALUT_PASS" > ~/project/ansible/.vault_password.txt
```
When you want to run the playbooks:
```yml
- run:
    name: Decrypt files and run playbooks
    command: cd ansible && ansible-playbook example.yml --vault-password-file .vault_password.txt
```



### Configuring Ansible

We use `ansible.cfg` to configure Ansible.

Example of relevant settings:

```
[defaults]
host_key_checking           = False
ansible_python_interpreter  = python3
inventory                   = hosts

[inventory]
enable_plugins              = ini
```

Needed the following for Ansible to read the `hosts` file (which parser it should use to read the file).

```
[inventory]
enable_plugins = ini
```

You might not need the last part of the config. Try running Ansible when removing the following part:

```
[ssh_connection]
ssh_args =
```

If you then get an error about "ssh and ControlSocket/permission denied for cp/ssh" add it again. You can read about the problem here, https://stackoverflow.com/a/41698903. There are supposed to be fixes for it but i can't get them to work.

You can also try to uncomment the line `# pipelining                  = True` to see if it still works. If it works Ansible should be faster.



### Run locally

When we want to work against an API, as the Azure modules do, we don't want Ansible to SSH to any server. So we connect to localhost without an ssh connection.

In `hosts` we need:

```
[local]
localhost ansible_connection=local
```

In the playbook to use the local host:

```
-   hosts: local
    connection: local # Keep ansible from open ssh connection
    gather_facts: False
```

When we run local plays we also need to change which Python interpreter should be used, to the one in our virtual environment. This is done in `groups_vars/local.yml`. With the line `ansible_python_interpreter: ../venv/bin/python`.


### Debugging and testing something out
Sometime you just want to test something, check value of a variable. You can do that with the following:

`ansible -m debug -a msg="{{playbook_dir}}" local`

Just replace `msg=""` with that you want to check. Examples of how this can be used inside a *playbook* can be found in the `provision_instances` tasks.

Use the `--verbose, -v` flag to enable verbose output for better debugging possibilities.   
Ansible has different stages of verbose, `-v` is for basic debugging, `-vvv` shows even more information and `-vvvv` enables connection debugging.

Example:
```bash
$ ansible-playbook site.yml -vvv
```

#### Encoding Error

If you get the following error:

```
File "microblog/venv/lib/python3.5/site-packages/boto/rds2/layer1.py", line 3779, in _make_request
  return json.loads(body)
File "/usr/lib/python3.5/json/__init__.py", line 312, in loads
  s.__class__.__name__))
TypeError: the JSON object must be str, not 'bytes'

.......

File \"microblog/venv/lib/python3.5/site-packages/boto/rds2/layer1.py\", line 1522, in describe_db_instances\n    path='/', params=params)\n  File \"../git/microblog/venv/lib/python3.5/site-packages/boto/rds2/layer1.py\", line 3779, in _make_request\n    return json.loads(body)\n  File \"/usr/lib/python3.5/json/__init__.py\", line 312, in loads\n    s.__class__.__name__))\nTypeError: the JSON object must be str, not 'bytes'\n",
    "module_stdout": "",
    "msg": "MODULE FAILURE\nSee stdout/stderr for the exact error",
    "rc": 1
}
```

Open the file `venv/lib/python3.5/site-packages/boto/rds2/layer1.py` and go to line 3779 (this can change), look for the line `return json.loads(body)`. Add a new line before that one with `body = response.read().decode('utf-8')`.

You can read about the error here, https://github.com/boto/boto/issues/2677.

#### Missing Modules
When you run a playbook after the time you install you dependencies, you might get an error pointing towards missing modules.

This is due to ether, one of our dependencies not being installed correctly or that you are running a non-compatible ansible version.

To fix this do the following:
1. Deactivate your `venv` and remove the folder.
2. Recreate it `python -m venv venv` and source it.
3. Reinstall the deploy dependencies `make install-deploy`.

If you do not have access to the `make` commands, install the dependencies normally `pip install -r requirements/deploy.txt`, followed by `pip install 'ansible[azure]'`.

The root cause of this issue is that we have a module called `ansible[azure]` in our `deploy.txt` file. This can in most cases be ignored and not installed when using the `pip install -r` command. This package contains a version based list of dependencies in which ansible needs to use when working with Azure.
