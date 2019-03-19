import hashlib as h
CACHE_DIR = './cache'
M = 20
main_func = 'sha512'
default_sleep_time = 1
default_chunk_size = 8 * 1024

def checksum(file_):
  hash_md5 = h.md5()
  with open(file_, "rb") as f:
    for chunk in iter(lambda: f.read(1024*1024), b""):
      hash_md5.update(chunk)
  return hash_md5.hexdigest()

def sha1(key):
  if not isinstance(key, bytes):
    key = key.encode()
  return int(h.sha1(key).hexdigest(), 16) %  2**M

def sha256(key):
  if not isinstance(key, bytes):
    key = key.encode()
  return int(h.sha256(key).hexdigest(), 16) %  2**M

def sha512(key):
  if not isinstance(key, bytes):
    key = key.encode()
  return int(h.sha512(key).hexdigest(), 16) %  2**M

def hash_(key):
  if not isinstance(key, bytes):
    key = key.encode()
  return abs(hash(key)) % 2**M

hash_funcs = {
  'sha1': sha1,
  'sha256': sha256,
  'sha512': sha512,
  'hash_': hash_
}
