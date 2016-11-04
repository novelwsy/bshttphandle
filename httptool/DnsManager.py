from CaseIgnoreDict import CaseIgnoreDict

hosts = CaseIgnoreDict()


def set(host):
    global hosts
    hosts.update(host)


def update(host):
    global hosts
    hosts.update(host)


def add(host, ip):
    global hosts
    if isinstance(host, dict):
        update(host)
    else:
        hosts[host] = ip


def clear():
    global hosts
    hosts.clear()


def remove(host):
    global hosts
    hosts.pop(host)


def resolve(host):
    if hosts.has_key(host):
        return hosts[host]
    else:
        return host


def load(hostfile):
    hostsconf = __import__(hostfile)
    if hasattr(hostsconf, 'hosts'):
        update(hostsconf.hosts)


import os

hostsfile = os.getcwd()
hostsfile = os.path.join(hostsfile, 'hosts.py')
if os.path.exists(hostsfile):
    print('load hosts configuration from %s' % hostsfile)
    load('hosts')
