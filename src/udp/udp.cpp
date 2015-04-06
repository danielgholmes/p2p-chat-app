#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

using namespace std;

int main()
{
    int sockfd, portno;
    int recvln;
    struct sockaddr_in peerAddr, myAddr;
    struct hostent *host;
    char *hostname = "localhost";
    char buffer[256];
    socklen_t addrlen = sizeof(peerAddr);
    portno = 5000;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        perror("Error opening socket!");
        return 0;
    }

    myAddr.sin_family = AF_INET;
    myAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    myAddr.sin_port = htons(portno);

    if (bind(sockfd, (struct sockaddr *)&myAddr, sizeof(myAddr)) < 0)
    {
        perror("Bind failed!");
        return 0;
    }

//    host = gethostbyname(hostname);
//    if (!host)
//    {
//        fprintf(stderr, "Could not obtain address of %s\n!", hostname);
//        return 0;
//    }
//
//    peerAddr.sin_family = AF_INET;
//    memcpy((void *)&peerAddr.sin_addr, host->h_addr_list[0], host->h_length);
//    peerAddr.sin_port = htons(portno);

    while(1)
    {
        printf("waiting on port %d\n", portno);
        recvln = recvfrom(sockfd, buffer, strlen(buffer), 0,(struct sockaddr *)&peerAddr, &addrlen);

        printf("received %d bytes\n", recvln);
        if (recvln > 0)
        {
            buffer[recvln] = 0;
            printf("received message: \"%s\"\n", buffer);
        }

        fgets(buffer,255,stdin);
        if (sendto(sockfd, buffer, strlen(buffer), 0, (struct sockaddr *)&peerAddr, sizeof(peerAddr)) < 0)
        {
            perror("Send failed!");
            return 0;
        }
    }

    close(sockfd);
    return 0;
}
