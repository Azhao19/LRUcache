#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

static void die(const char *s) { perror(s); exit(1); }

int main(int argc, char **argv)
{
    if (argc != 4) {
        fprintf(stderr, "usage: <host> <server-port> <file-path>\n");
        exit(1);
    }

    struct hostent *he;
    char *serverName = argv[1];
    
    if ((he = gethostbyname(serverName)) == NULL) {
        die("gethostbyname failed");
    }

    char *ip = inet_ntoa(*(struct in_addr *) he->h_addr);

    unsigned short port = atoi(argv[2]);

    // Create a socket for TCP connection

    int sock; // socket descriptor
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        die("socket failed");

    // Construct a server address structure

    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof(servaddr)); // must zero out the structure
    servaddr.sin_family      = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr(ip);
    servaddr.sin_port        = htons(port); // must be in network byte order

    // Establish a TCP connection to the server

    if (connect(sock, (struct sockaddr *) &servaddr, sizeof(servaddr)) < 0)
        die("connect failed");

    // Read a line from stdin and send it to the server

    char buf[1000];
    snprintf(buf, sizeof(buf), "GET %s HTTP/1.0\r\nHost:%s:%s\r\n\r\n", argv[3], serverName, argv[2]);
    if (send(sock, buf, strlen(buf), 0) != strlen(buf)) {
        die("send failed");
    }
    
    FILE *read = fdopen(sock, "r");
    if (read == NULL) {
        die("fopen failed");
    }

    int line = 1;
    while (strcmp(fgets(buf, sizeof(buf), read), "\r\n") && strcmp(buf, "\n")) {
        if (line == 1 && (strstr(buf, "200") == NULL)) {
            fclose(read);
            fprintf(stderr, "%s\n", buf);
            exit(1);
        }
        line++;
    }
    if (ferror(read)) {
        fclose(read);
        die("recv failed");
    }
    char *filename = *(strrchr(argv[3], '/') + 1) != '\0' ? strrchr(argv[3], '/') + 1 : "default";
    FILE *writeTo = fopen(filename, "wb");
    if (writeTo == NULL) {
        die("fopen failed");
    }

    int r;
    while ((r = fread(buf, 1, sizeof(buf), read)) > 0) { 
        fwrite(buf, 1, r, writeTo);
    }
    if (ferror(read) || ferror(writeTo)) {
        die("something failed");
    }
    fclose(writeTo);
    fclose(read);
    return 0;
}
