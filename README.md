# hamachi-ssh
*for Linux and OSX*

[LogMeIn Hamachi](https://secure.logmein.com/home) is a simple, excellent VPN solution. The clients for Linux and OSX expose a commandline interface. *hamachi-ssh* is a utility that uses information from the client to update your SSH config file, so you can SSH to your remote machines on the network using their Hamachi names. For example, if the machine's name is `battlestation`, instead of checking its IP and using that you can simply do:

    ssh user@battlestation
    
There are other ways in which the config file makes your life with SSH simpler. Check out DigitalOcean's [article](https://www.digitalocean.com/community/tutorials/how-to-configure-custom-connection-options-for-your-ssh-client) for more.

## Installation and usage
Install via [pip](https://pip.pypa.io/en/stable/installing/), the Python package manager:

    pip install hamachi-ssh

To update your SSH config file, just do:

    hamachi-ssh-update

By default, it updates the config file at `~/.ssh/config`. If you want another path, pass it as the argument to the command.

The main purpose of *hamachi-ssh* is to keep your Hamachi IPs in the config file updated, since they can change frequently. If there are new clients on the network, *hamachi-ssh* will generate new simple entries for them as well.
