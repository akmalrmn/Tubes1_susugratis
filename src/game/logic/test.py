def hitung_diamonds_berdekatan_recursively(koordinat, kotak, visited):
    x, y = koordinat
    # Jika koordinat sudah pernah dikunjungi atau berada di luar kotak, kembalikan 0
    if koordinat in visited or x < 0 or x >= len(kotak) or y < 0 or y >= len(kotak[0]):
        return 0
    
    # Tandai koordinat sebagai sudah dikunjungi
    visited.add(koordinat)
    
    # Jika koordinat ini merupakan diamond
    if kotak[x][y] == 0:
        # Jika diamond berwarna merah, tambahkan 1, jika berwarna biru, tambahkan 2
        return 0
    
    # Jumlah diamonds berdekatan dari koordinat sekitarnya
    return kotak[x][y] + hitung_diamonds_berdekatan_recursively((x, y + 1), kotak, visited) + hitung_diamonds_berdekatan_recursively((x, y - 1), kotak, visited) + hitung_diamonds_berdekatan_recursively((x + 1, y), kotak, visited) + hitung_diamonds_berdekatan_recursively((x - 1, y), kotak, visited)

# Contoh penggunaan fungsi rekursif
kotak = [[0] * 15 for _ in range(15)]  # Inisialisasi kotak berukuran 15x15 dengan nilai awal 0

# Misalkan diamonds berwarna merah (value ditambah 1)
diamonds_merah = [(2,3),(3,3),(4,3),(3,4),(4,4)]

# Misalkan diamonds berwarna biru (value ditambah 2)
diamonds_biru = [(4,5),(8, 8),(8,9),(9,8),(9,9)]

# Set nilai diamonds berwarna merah menjadi 1 di kotak
for x, y in diamonds_merah:
    kotak[x][y] = 1

# Set nilai diamonds berwarna biru menjadi 2 di kotak
for x, y in diamonds_biru:
    kotak[x][y] = 2

# Inisialisasi set untuk menyimpan koordinat yang sudah dikunjungi
visited = set()

# Hitung jumlah diamonds berdekatan untuk diamonds berwarna merah
print("Jumlah diamonds berdekatan untuk diamonds merah dan biru:", hitung_diamonds_berdekatan_recursively((3, 3), kotak, visited))

