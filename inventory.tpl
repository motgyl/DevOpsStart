[frontend]
%{ for name in frontend_names ~}
root@${name}@orb ansible_user=root@${name} orb_domain=${name}.orb.local
%{ endfor ~}

[backend]
%{ for name in backend_names ~}
root@${name}@orb ansible_user=root@${name} orb_domain=${name}.orb.local
%{ endfor ~}

[db]
%{ for name in db_names ~}
root@${name}@orb ansible_user=root@${name} orb_domain=${name}.orb.local
%{ endfor ~}

