#include <unistd.h>

ssize_t myread(char *buf, size_t size){
    ssize_t result;
    result = read(STDIN_FILENO, buf, size);
    if(result > 0 && result <= size){
        for(int i=0; i < result; i++){
            if(i%2) buf[i] = '?';
        }
        buf[result] = 0;
    }
    return result;
}

int main(){
    char mybuf[42];
    ssize_t result;
    result = myread(mybuf, sizeof(mybuf));
    return 0;
}
