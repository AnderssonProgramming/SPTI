#include <stdio.h>
#include <string.h>

// Function to validate the key (matches the 'Function Analysis' phase of your guide)
int check_pass(char *input) {
    // This is the hardcoded string you will look for using the 'strings' command
    char secret[] = "ECI_Security_2026"; 
    return strcmp(input, secret);
}

int main() {
    char buffer[64];
    printf("--- ECI Banking System Auth ---\n");
    printf("Enter the master key: ");
    scanf("%63s", buffer);

    // Conditional logic (matches the 'Conditional analysis' phase of your guide)
    // In assembly, this will trigger the TEST and JNE/JE instructions
    if (check_pass(buffer) == 0) {
        printf("\n[+] ACCESS GRANTED. Welcome, Admin.\n");
    } else {
        printf("\n[-] ERROR: Incorrect key. System alert sent.\n");
    }
    
    return 0;
}