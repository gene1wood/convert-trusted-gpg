import re
import subprocess


def get_valid_filename(name):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'

    https://github.com/django/django/blob/main/django/utils/text.py
    """
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "", s)
    if s in {"", ".", ".."}:
        raise Exception("Could not derive file name from '%s'" % name)
    return s


def main():
    result = subprocess.run(["apt-key", "list"], text=True, capture_output=True)
    lines = result.stdout.splitlines()
    action = None
    line_type = None
    fingerprint = None
    keys = {}
    for line in lines:
        if line == '/etc/apt/trusted.gpg':
            action = "collect trusted.gpg keys"
            continue
        if action == "collect trusted.gpg keys" and line.startswith('/etc/apt/trusted.gpg.d/'):
            action = "collect trusted.gpg.d files"
        if line.startswith('/etc/apt/trusted.gpg.d/'):
            line_type = 'filename'
            continue
        if line.startswith('pub '):
            line_type = 'pub'
            continue
        if line_type == 'pub':
            # This is the line after a 'pub' line
            line_type = 'key'
            fingerprint = line.replace(' ', '')
            continue
        if line.startswith('uid '):
            line_type = 'uid'
            if action == "collect trusted.gpg keys":
                uid = get_valid_filename(line.split('] ', 1)[1])
                keys[fingerprint] = uid
                continue
            if action == "collect trusted.gpg.d files":
                if fingerprint in keys:
                    # This key already exists in /etc/apt/trusted.gpg.d/
                    print(f'Skipping {fingerprint} as it already exists in /etc/apt/trusted.gpg.d/')
                    del keys[fingerprint]

    for fingerprint in keys:
        print(f'Creating /etc/apt/trusted.gpg.d/{keys[fingerprint]}.asc')
        result = subprocess.run(["apt-key", "export", fingerprint], text=True, capture_output=True)
        with open(f'/etc/apt/trusted.gpg.d/{keys[fingerprint]}.asc', 'w') as f:
            f.write(result.stdout)
