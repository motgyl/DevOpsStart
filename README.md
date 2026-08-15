# First Terraform & Ansible project

## Installation
### macOS

`brew install hashicorp/tap/terraform
### ubuntu

`sudo apt install terraform`

---

`terraform --version`

---
### Config tf example
simple website project, three components: backend, frontend, database

```tf
terraform {
  required_providers {
    orbstack = {
      source = "robertdebock/orbstack"
      }
    }
}

resource "orbstack_machine" "backend" {
  count = 2
  name = "backend-${count.index + 1}"
  image = "ubuntu:24.04"
}

resource "orbstack_machine" "frontend" {
  count = 2
  name = "frontend-${count.index + 1}"
  image = "ubuntu:24.04"
}

resource "orbstack_machine" "db" {
  count = 2
  name = "db-${count.index + 1}"
  image = "ubuntu:24.04"
}
```

### Initialisation 

`terraform init`

###  Planing

`terraform plan`
### Running

`terraform apply`
confirming terraform plan (6 to add, 0 to change, 0 to destroy)

### Status

```zsh
❯ terraform show
# orbstack_machine.backend[0]:
resource "orbstack_machine" "backend" {
    default_machine = true
    id              = "backend-1"
    image           = "ubuntu:24.04"
    ip_address      = "192.168.139.119"
    name            = "backend-1"
    ssh_host        = "192.168.139.119"
    ssh_port        = 22
    status          = "running"
}

# orbstack_machine.backend[1]:
resource "orbstack_machine" "backend" {
    default_machine = false
    id              = "backend-2"
    image           = "ubuntu:24.04"
    ip_address      = "192.168.139.158"
    name            = "backend-2"
    ssh_host        = "192.168.139.158"
    ssh_port        = 22
    status          = "running"
}

# orbstack_machine.db[0]:
resource "orbstack_machine" "db" {
    default_machine = false
    id              = "db-1"
    image           = "ubuntu:24.04"
    ip_address      = "192.168.139.114"
    name            = "db-1"
    ssh_host        = "192.168.139.114"
    ssh_port        = 22
    status          = "running"
}

# orbstack_machine.db[1]:
resource "orbstack_machine" "db" {
    default_machine = false
    id              = "db-2"
    image           = "ubuntu:24.04"
    ip_address      = "192.168.139.21"
    name            = "db-2"
    ssh_host        = "192.168.139.21"
    ssh_port        = 22
    status          = "running"
}

# orbstack_machine.frontend[0]:
resource "orbstack_machine" "frontend" {
    default_machine = false
    id              = "frontend-1"
    image           = "ubuntu:24.04"
    ip_address      = "192.168.139.99"
    name            = "frontend-1"
    ssh_host        = "192.168.139.99"
    ssh_port        = 22
    status          = "running"
}

# orbstack_machine.frontend[1]:
resource "orbstack_machine" "frontend" {
    default_machine = false
    id              = "frontend-2"
    image           = "ubuntu:24.04"
    ip_address      = "192.168.139.47"
    name            = "frontend-2"
    ssh_host        = "192.168.139.47"
    ssh_port        = 22
    status          = "running"
}
```
### Destroing

`terraform destroy`

### Ansible installation 

`brew install ansible`

### Testing Ansible access

`ansible -i inventory.ini all -m ping`


