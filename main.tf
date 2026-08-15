terraform {
  required_providers {
    orbstack = {
      source = "robertdebock/orbstack"
    }
    local = {
      source = "hashicorp/local"
      version = "~> 2.5"
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

locals {
   frontend_names = [for m in orbstack_machine.frontend : m.name]
   backend_names = [for m in orbstack_machine.backend: m.name]
   db_names = [for m in orbstack_machine.db: m.name]
 }


 resource "local_file" "ansible_inventory" {
   filename = "${path.module}/inventory.ini"
   content = templatefile("${path.module}/inventory.tpl", {
     frontend_names = local.frontend_names
     backend_names = local.backend_names
     db_names = local.db_names
   })
 }
