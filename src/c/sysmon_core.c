// src/c/sysmon_core.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/statvfs.h>

// Função para obter CPU usando top (versão melhorada)
double get_cpu_usage() {
    // Tenta diferentes padrões de busca
    const char *patterns[] = {
        "top -bn1 | grep -i 'cpu:' | head -1",
        "top -bn1 | grep '%Cpu' | head -1",
        "top -bn1 | head -4 | tail -1",
        NULL
    };
    
    for (int i = 0; patterns[i] != NULL; i++) {
        FILE *fp = popen(patterns[i], "r");
        if (!fp) continue;
        
        char line[256];
        if (fgets(line, sizeof(line), fp)) {
            // Procura por números seguidos de %
            char *p = line;
            while (*p) {
                if (*p == '%' && p > line) {
                    // Volta até encontrar o início do número
                    char *start = p - 1;
                    while (start > line && (*start == ' ' || *start == '\t' || 
                           (*start >= '0' && *start <= '9') || *start == '.')) {
                        start--;
                    }
                    start++;
                    
                    // Converte para double
                    double val = atof(start);
                    if (val > 0 && val <= 100) {
                        pclose(fp);
                        return val;
                    }
                }
                p++;
            }
        }
        pclose(fp);
    }
    
    // Último recurso: tenta ler diretamente do /proc/stat (se permitido)
    FILE *fp = fopen("/proc/stat", "r");
    if (fp) {
        char line[256];
        if (fgets(line, sizeof(line), fp)) {
            // Formato: "cpu  user nice system idle ..."
            long long user, nice, system, idle;
            if (sscanf(line, "cpu %lld %lld %lld %lld", &user, &nice, &system, &idle) == 4) {
                long long total = user + nice + system + idle;
                fclose(fp);
                
                // Segunda leitura após 0.5s
                usleep(500000);
                fp = fopen("/proc/stat", "r");
                if (fp) {
                    if (fgets(line, sizeof(line), fp)) {
                        long long user2, nice2, system2, idle2;
                        if (sscanf(line, "cpu %lld %lld %lld %lld", &user2, &nice2, &system2, &idle2) == 4) {
                            long long total2 = user2 + nice2 + system2 + idle2;
                            long long total_diff = total2 - total;
                            long long idle_diff = (idle2 - idle);
                            
                            if (total_diff > 0) {
                                double usage = 100.0 * (total_diff - idle_diff) / total_diff;
                                fclose(fp);
                                return usage;
                            }
                        }
                    }
                    fclose(fp);
                }
            } else {
                fclose(fp);
            }
        } else {
            fclose(fp);
        }
    }
    
    return -1.0;  // Não conseguiu obter
}

// Memória via /proc/meminfo
void get_memory(long *total_kb, long *available_kb) {
    FILE *fp = fopen("/proc/meminfo", "r");
    if (!fp) {
        *total_kb = *available_kb = -1;
        return;
    }
    
    char line[256];
    *total_kb = *available_kb = -1;
    
    while (fgets(line, sizeof(line), fp)) {
        if (strncmp(line, "MemTotal:", 9) == 0) {
            sscanf(line, "%*s %ld", total_kb);
        } else if (strncmp(line, "MemAvailable:", 13) == 0) {
            sscanf(line, "%*s %ld", available_kb);
        }
    }
    
    fclose(fp);
}

// Armazenamento via statvfs
void get_storage(unsigned long *total, unsigned long *free) {
    struct statvfs vfs;
    if (statvfs("/data", &vfs) == 0) {
        *total = vfs.f_blocks * vfs.f_frsize;
        *free = vfs.f_bfree * vfs.f_frsize;
    } else {
        *total = *free = 0;
    }
}

int main() {
    double cpu = get_cpu_usage();
    long mem_total_kb = -1, mem_avail_kb = -1;
    get_memory(&mem_total_kb, &mem_avail_kb);
    unsigned long storage_total = 0, storage_free = 0;
    get_storage(&storage_total, &storage_free);
    
    printf("{\n");
    
    // CPU
    if (cpu > 0) {
        printf("  \"cpu_pct\": %.1f,\n", cpu);
    } else {
        printf("  \"cpu_pct\": \"?\",\n");
    }
    
    // Memória
    if (mem_total_kb > 0 && mem_avail_kb > 0) {
        long mem_used_kb = mem_total_kb - mem_avail_kb;
        double mem_pct = 100.0 * mem_used_kb / mem_total_kb;
        printf("  \"mem_pct\": %.1f,\n", mem_pct);
        printf("  \"mem_used_mb\": %ld,\n", mem_used_kb / 1024);
        printf("  \"mem_total_mb\": %ld,\n", mem_total_kb / 1024);
    } else {
        printf("  \"mem_pct\": \"?\",\n");
        printf("  \"mem_used_mb\": \"?\",\n");
        printf("  \"mem_total_mb\": \"?\",\n");
    }
    
    // Armazenamento
    if (storage_total > 0) {
        unsigned long storage_used = storage_total - storage_free;
        double storage_pct = 100.0 * storage_used / storage_total;
        printf("  \"storage_total\": %lu,\n", storage_total);
        printf("  \"storage_used\": %lu,\n", storage_used);
        printf("  \"storage_pct\": %.1f\n", storage_pct);
    } else {
        printf("  \"storage_total\": 0,\n");
        printf("  \"storage_used\": 0,\n");
        printf("  \"storage_pct\": 0.0\n");
    }
    
    printf("}\n");
    return 0;
}
