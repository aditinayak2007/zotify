#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <sys/wait.h>

#define MAX_LINE 256

static void print_menu(void)
{
    printf("\n=========== SIMULATOR ===========\n");
    printf("Type a command and press Enter.\n");
    printf("Examples (match these with Core's commands):\n");
    printf("  ADD 10 20        - CPU operation\n");
    printf("  STORE 5 99       - write to memory\n");
    printf("  LOAD 5           - read from memory\n");
    printf("  PUSH 7 / POP     - stack operations\n");
    printf("  ENQ 3 / DEQ      - queue operations\n");
    printf("  HELP             - show this menu\n");
    printf("  EXIT             - quit the simulator\n");
    printf("=================================\n");
}

/* remove trailing newline / spaces, skip leading spaces; returns start of text */
static char *trim(char *s)
{
    while (isspace((unsigned char)*s))
        s++;
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1]))
        s[--n] = '\0';
    return s;
}

/* make the command word upper case so "add" and "ADD" both work */
static void upper_first_word(char *s)
{
    for (; *s && !isspace((unsigned char)*s); s++)
        *s = (char)toupper((unsigned char)*s);
}

/*
 * ui_process: runs the whole UI loop.
 *   to_core   - write end of the UI -> Core pipe
 *   from_core - read end of the Core -> UI pipe
 * Returns 0 on normal exit, -1 on a pipe error.
 */
int ui_process(int to_core, int from_core)
{
    FILE *out = fdopen(to_core, "w");
    FILE *in  = fdopen(from_core, "r");
    if (!out || !in) {
        perror("UI: fdopen");
        return -1;
    }

    char raw[MAX_LINE];
    char reply[MAX_LINE];

    print_menu();

    while (1) {
        printf("\nsim> ");
        fflush(stdout);

        /* 1. read user input (Ctrl+D = exit) */
        if (!fgets(raw, sizeof raw, stdin)) {
            printf("\nEnd of input. Exiting.\n");
            break;
        }

        /* line too long? (no newline and not end of file) */
        if (!strchr(raw, '\n') && !feof(stdin)) {
            int c;
            while ((c = getchar()) != '\n' && c != EOF)
                ;
            printf("Error: command too long (max %d characters).\n", MAX_LINE - 2);
            continue;
        }

        /* 2. clean and validate */
        char *cmd = trim(raw);
        if (*cmd == '\0') {
            printf("Please enter a command (type HELP for the list).\n");
            continue;
        }
        upper_first_word(cmd);

        /* 3. commands handled by the UI itself */
        if (strcmp(cmd, "HELP") == 0) {
            print_menu();
            continue;
        }

        /* 4. send to Core */
        if (fprintf(out, "%s\n", cmd) < 0 || fflush(out) == EOF) {
            printf("Error: could not send to Core (pipe closed).\n");
            fclose(out);
            fclose(in);
            return -1;
        }

        if (strcmp(cmd, "EXIT") == 0) {
            printf("Exiting simulator...\n");
            break;
        }

        /* 5. wait for Core's reply */
        if (!fgets(reply, sizeof reply, in)) {
            printf("Error: Core stopped responding.\n");
            fclose(out);
            fclose(in);
            return -1;
        }

        /* 6. display result */
        printf("Result: %s", reply);
        if (strchr(reply, '\n') == NULL)
            printf("\n");
    }

    fclose(out);   /* closing the pipe tells Core we are done */
    fclose(in);
    return 0;
}

/* ------------------------------------------------------------------ */
/* Stand-alone test: a fake Core that just echoes, so you can test    */
/* the UI before the real Core and pipes from the team are ready.      */
/* ------------------------------------------------------------------ */
#ifdef UI_STANDALONE
int main(void)
{
    int ui_to_core[2], core_to_ui[2];
    if (pipe(ui_to_core) == -1 || pipe(core_to_ui) == -1) {
        perror("pipe");
        return 1;
    }

    pid_t pid = fork();
    if (pid == -1) {
        perror("fork");
        return 1;
    }

    if (pid == 0) {                       /* fake Core */
        close(ui_to_core[1]);
        close(core_to_ui[0]);
        FILE *rd = fdopen(ui_to_core[0], "r");
        FILE *wr = fdopen(core_to_ui[1], "w");
        char line[MAX_LINE];
        while (fgets(line, sizeof line, rd)) {
            line[strcspn(line, "\n")] = '\0';
            if (strcmp(line, "EXIT") == 0)
                break;
            fprintf(wr, "[fake core] got: %s\n", line);
            fflush(wr);
        }
        return 0;
    }

    /* UI (parent) */
    close(ui_to_core[0]);
    close(core_to_ui[1]);
    int rc = ui_process(ui_to_core[1], core_to_ui[0]);
    wait(NULL);
    return rc == 0 ? 0 : 1;
}
#endif
