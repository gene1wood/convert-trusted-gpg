# convert-trusted-gpg

This tool read the [APT](https://en.wikipedia.org/wiki/APT_(software)) key store's single
file and creates multiple files, one for each key.

Doing this will prevent the deprecation warning when running `apt update`

> `W: https://example.com/ubuntu/dists/jammy/InRelease: Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg), see the DEPRECATION section in apt-key(8) for details.`

The tool accomplishes this by 

1. Reading all the keys inside the `/etc/apt/trusted.gpg` file
2. For each key, if that key doesn't exist in its own file in `/etc/apt/trusted.gpg.d/`,
   the tool creates a new file in the `trusted.gpg.d` directory containing the key

The tool bases the new file's filename on the name and email address of the key.

The tool assumes that `apt` version `>=1.4` is installed which supports ASCII armored keys
with an `.asc` extension instead of binary keys with a `.gpg` extension.

## Usage

```shell
sudo convert-trusted-gpg
```

## Example output

```text
Skipping 1EDDE2CDFC025D17F6DA9EC0ADAE6AD28A8F901A as it already exists in /etc/apt/trusted.gpg.d/
Skipping 37C84554E7E0A261E4F76E1ED26E6ED000654A3E as it already exists in /etc/apt/trusted.gpg.d/
Creating /etc/apt/trusted.gpg.d/WineHQ_packages_wine-develwinehq.org.asc
Creating /etc/apt/trusted.gpg.d/NodeSource_gpgnodesource.com.asc
```