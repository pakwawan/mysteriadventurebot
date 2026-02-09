#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THE MYSTERY ADVENTURE BOT
Pencarian Harta Karun di Bantul, DIY
A Text-Based Adventure Game
"""

import random
import time
import json
from typing import Dict, List, Tuple

class MysteryAdventureGame:
    def __init__(self):
        self.player_name = ""
        self.inventory = []
        self.health = 100
        self.money = 50000  # Rupiah
        self.current_location = "bandara"
        self.visited_locations = set()
        self.npcs_met = set()
        self.clues_found = []
        self.game_state = {}
        self.treasure_found = False
        self.game_over = False
        
        # Map lokasi di Bantul
        self.locations = {
            "bandara": {
                "name": "Bandara Adisumarmo",
                "desc": "Anda baru tiba di Bandara Adisumarmo. Perjalanan Anda menuju Bantul untuk mencari harta karun legendaris dimulai di sini.",
                "exits": {"timur": "jejeran", "barat": "jalan_utama"}
            },
            "jalan_utama": {
                "name": "Jalan Utama Bantul",
                "desc": "Jalan raya utama Bantul yang ramai dengan kendaraan dan pedagang. Anda melihat beberapa toko antik lokal.",
                "exits": {"timur": "bandara", "utara": "pasar_tradisional", "selatan": "desa_kulon"}
            },
            "pasar_tradisional": {
                "name": "Pasar Tradisional Bantul",
                "desc": "Pasar tradisional yang sibuk dengan pedagang menjual berbagai barang. Ada seorang tua misterius yang menjual peta kuno.",
                "npc": "penjual_peta",
                "exits": {"selatan": "jalan_utama", "timur": "taman_prambanan"}
            },
            "taman_prambanan": {
                "name": "Candi Prambanan Area",
                "desc": "Area Candi Prambanan - situs warisan dunia UNESCO. Kuil-kuil megah berdiri kokoh. Anda merasakan energi mistis di tempat ini.",
                "npc": "pendeta_candi",
                "exits": {"barat": "pasar_tradisional", "selatan": "gua_misteri"}
            },
            "gua_misteri": {
                "name": "Gua Misteri Bantul",
                "desc": "Gua gelap dan dingin di sekitar Bantul. Anda mendengar suara aneh bergema di dalam. Ini bisa jadi tempat penyimpanan harta karun kuno.",
                "exits": {"utara": "taman_prambanan", "dalam": "dalam_gua"},
                "danger": True
            },
            "dalam_gua": {
                "name": "Dalam Gua - Ruang Penyimpanan",
                "desc": "Ruang dalam yang lebih gelap. Dinding gua penuh dengan tulisan kuno dan simbol-simbol aneh. Anda menemukan altar kuno.",
                "exits": {"keluar": "gua_misteri"},
                "treasure_spot": True
            },
            "desa_kulon": {
                "name": "Desa Kulon - Desa Tradisional",
                "desc": "Desa tradisional Bantul yang masih mempertahankan budaya kuno. Rumah-rumah bergaya Jawa berdiri di antara pepohonan rindang.",
                "npc": "kepala_desa",
                "exits": {"utara": "jalan_utama", "timur": "jejeran"}
            },
            "jejeran": {
                "name": "Jejeran - Pegunungan Bantul",
                "desc": "Pegunungan hijau di Bantul. Pemandangan spektakuler menyambut Anda. Konon ada petunjuk harta karun tersembunyi di puncak.",
                "exits": {"barat": "desa_kulon", "atas": "puncak_gunung"}
            },
            "puncak_gunung": {
                "name": "Puncak Gunung Jejeran",
                "desc": "Puncak gunung yang tinggi dengan pemandangan Yogyakarta. Anda menemukan batu bertulis yang sangat tua.",
                "exits": {"bawah": "jejeran"},
                "clue": True
            },
            "makam_raja": {
                "name": "Makam Raja Kuno",
                "desc": "Makam berusia ratusan tahun dari dinasti kuno. Tempat ini penuh misteri dan ketenangan. Konon si raja menyembunyikan treasure di sini sebelum wafat.",
                "npc": "penjaga_makam",
                "exits": {"keluar": "jalan_utama"},
                "treasure_spot": True
            }
        }
        
        # NPC dan dialogue
        self.npcs = {
            "penjual_peta": {
                "name": "Pak Dukuh (Penjual Peta Kuno)",
                "intro": "Seorang tua dengan rambut putih menyalamimu dengan wajah penuh teka-teki.",
                "dialogues": [
                    "Halo anak muda, kelihatannya kamu mencari sesuatu yang berharga?",
                    "Saya tahu tentang harta karun legendaris di Bantul...",
                    "Peta kuno ini sangat langka. Hanya 500 ribu rupiah!"
                ],
                "item": "Peta Kuno Bantul"
            },
            "pendeta_candi": {
                "name": "Pendeta Candi (Penjaga Warisan)",
                "intro": "Seorang pendeta tua dengan pakaian putih berdiri tenang di depan candi.",
                "dialogues": [
                    "Selamat datang di Candi Prambanan, tempat suci...",
                    "Harta karun sejati bukanlah emas, tapi kebijaksanaan...",
                    "Namun jika kamu ingin mencari emas, dengarkan petunjuk ini: cari di tempat yang paling tua dan gelap..."
                ],
                "item": "Mantra Perlindungan Kuno"
            },
            "kepala_desa": {
                "name": "Kepala Desa Kulon - Bapak Subroto",
                "intro": "Kepala desa yang berwibawa menyapamu dengan ramah.",
                "dialogues": [
                    "Selamat datang di Desa Kulon kami...",
                    "Aku mendengar kabar tentang pencarian harta karun mu...",
                    "Ada legenda kuno tentang harta yang disimpan di makam tua, ke selatan desa kami..."
                ],
                "item": "Kunci Tua Makam"
            },
            "penjaga_makam": {
                "name": "Penjaga Makam - Mbah Tarpem",
                "intro": "Seorang penjaga makam tua dengan wajah garang tapi hati baik.",
                "dialogues": [
                    "Siapa yang berani datang ke makam suci ini?",
                    "Jika kamu menghormati leluhur, aku akan membantu...",
                    "Gunakan kunci itu untuk membuka peti harta karun di bawah tanah makam..."
                ],
                "item": "Petunjuk Peti Harta"
            }
        }
        
        self.intro_text = """
╔════════════════════════════════════════════════╗
║   THE MYSTERY ADVENTURE BOT                    ║
║   Pencarian Harta Karun di Bantul, Yogyakarta  ║
╚════════════════════════════════════════════════╝

Legenda kuno menceritakan tentang harta karun besar yang disembunyikan
di wilayah Bantul, Daerah Istimewa Yogyakarta. Harta tersebut berasal
dari dinasti kuno yang pernah berkuasa ratusan tahun lalu.

Sebagai seorang petualang, Anda memiliki peta dan pengetahuan tentang
lokasi-lokasi bersejarah. Kini saatnya untuk memulai perjalanan
mencari harta karun terbesar sepanjang masa!

Namun hati-hati... Perjalanan ini penuh dengan misteri, tantangan,
dan kejutan tak terduga!
        """

    def print_banner(self):
        """Cetak banner game"""
        print("\n" + "="*55)
        print(self.intro_text)
        print("="*55 + "\n")

    def get_player_input(self, prompt: str) -> str:
        """Dapatkan input dari pemain"""
        user_input = input(f"\n{prompt} > ").strip().lower()
        return user_input

    def start_game(self):
        """Mulai permainan"""
        self.print_banner()
        
        # Dapatkan nama pemain
        name_input = input("Siapa nama Anda, petualang? ")
        if not name_input.strip():
            name_input = "Petualang Misterius"
        self.player_name = name_input
        
        print(f"\n✨ Selamat datang {self.player_name}! ✨")
        print("Perjalanan Anda menuju Bantul dimulai...\n")
        time.sleep(2)
        
        self.main_game_loop()

    def show_status(self):
        """Tampilkan status pemain"""
        print(f"\n{'='*50}")
        print(f"📍 LOKASI: {self.locations[self.current_location]['name']}")
        print(f"❤️  KESEHATAN: {self.health}%")
        print(f"💰 UANG: Rp {self.money:,}")
        print(f"🎒 INVENTORI ({len(self.inventory)}): {', '.join(self.inventory) if self.inventory else 'Kosong'}")
        print(f"🔍 PETUNJUK DITEMUKAN: {len(self.clues_found)}")
        print(f"{'='*50}")

    def show_location(self):
        """Tampilkan deskripsi lokasi"""
        location = self.locations[self.current_location]
        print(f"\n📍 {location['name']}")
        print(f"   {location['desc']}")
        
        if location.get('npc'):
            npc_key = location['npc']
            print(f"   👤 Ada {self.npcs[npc_key]['name']} di sini!")
        
        # Peringatan bahaya
        if location.get('danger'):
            print("   ⚠️  PERINGATAN: Tempat ini berbahaya!")
        
        self.visited_locations.add(self.current_location)

    def show_exits(self):
        """Tampilkan pilihan keluar"""
        exits = self.locations[self.current_location]['exits']
        print("\n🚪 Kemana Anda ingin pergi?")
        for direction, location in exits.items():
            print(f"   - {direction}: {self.locations[location]['name']}")
        print("   - perintah (untuk bantuan)")
        print("   - status (lihat status pemain)")
        print("   - lihat_npc (bicara dengan NPC)")

    def interact_with_npc(self):
        """Berinteraksi dengan NPC"""
        location = self.locations[self.current_location]
        if not location.get('npc'):
            print("❌ Tidak ada NPC di lokasi ini.")
            return
        
        npc_key = location['npc']
        npc = self.npcs[npc_key]
        
        if npc_key in self.npcs_met:
            print(f"\n👤 {npc['name']}: 'Kita sudah bertemu sebelumnya, ingat?'")
            return
        
        print(f"\n👤 {npc['name']}")
        print(f"   {npc['intro']}\n")
        
        # Tampilkan dialog
        for dialogue in npc['dialogues']:
            print(f"   💬 {dialogue}")
            time.sleep(1)
        
        # Tawarkan item
        item = npc['item']
        print(f"\n   {npc['name']} memberikan Anda: {item}")
        self.inventory.append(item)
        self.npcs_met.add(npc_key)
        
        # Berikan clue atau kurangi uang
        if "Peta" in item:
            cost = 500000
            if self.money >= cost:
                self.money -= cost
                print(f"   💰 Anda membayar Rp {cost:,}")
                self.clues_found.append(f"Peta dari {npc['name']}")
            else:
                print(f"   ❌ Anda tidak punya uang cukup! (Butuh Rp {cost:,})")
                self.inventory.remove(item)
        else:
            self.clues_found.append(f"Petunjuk dari {npc['name']}")

    def explore_location(self):
        """Jelajahi lokasi untuk mencari clue"""
        location = self.locations[self.current_location]
        
        if location.get('clue'):
            clue = "Tulisan kuno: 'Makam leluhur menyimpan harta yang tak ternilai. Cari kunci di pasar kuno.'"
            print(f"\n🔍 Anda menemukan sesuatu!")
            print(f"   {clue}")
            self.clues_found.append(clue)
            return True
        
        if location.get('treasure_spot'):
            if "Kunci Tua Makam" in self.inventory:
                self.show_treasure()
                return
            else:
                print("\n🔍 Anda melihat pintu terkunci dengan kunci tua...")
                print("   ⚠️  Anda membutuhkan Kunci Tua untuk membuka ini!")
                return
        
        print("\n🔍 Anda melihat-lihat sekitar tapi tidak menemukan apa-apa yang menarik.")

    def show_treasure(self):
        """Tampilkan penemuan harta karun"""
        self.treasure_found = True
        
        print("\n" + "🎉"*20)
        print("""
╔═══════════════════════════════════════════════════╗
║           ANDA MENEMUKAN HARTA KARUN!             ║
╚═══════════════════════════════════════════════════╝

Peti emas besar terlihat berkilau di hadapan Anda!
        """)
        print("🎉"*20)
        
        treasure_options = [
            ("Bawa semua harta", 5000000),
            ("Ambil sebagian saja", 2000000),
            ("Laporkan ke pemerintah", 1000000)
        ]
        
        print("\nApa yang Anda lakukan?")
        for i, (option, reward) in enumerate(treasure_options, 1):
            print(f"{i}. {option}")
        
        while True:
            choice = self.get_player_input("Pilihan Anda (1-3)")
            if choice in ['1', '2', '3']:
                idx = int(choice) - 1
                reward = treasure_options[idx][1]
                self.money += reward
                
                if idx == 0:
                    print(f"\n✨ Anda mengambil semua harta! +Rp {reward:,}")
                    self.game_state['ending'] = 'greedy'
                elif idx == 1:
                    print(f"\n✨ Anda mengambil sebagian harta dengan bijak! +Rp {reward:,}")
                    self.game_state['ending'] = 'balanced'
                else:
                    print(f"\n✨ Anda melaporkan penemuan ini! Pemerintah memberi reward! +Rp {reward:,}")
                    self.game_state['ending'] = 'hero'
                
                self.game_over = True
                break
            else:
                print("❌ Pilihan tidak valid!")

    def show_help(self):
        """Tampilkan bantuan"""
        print("""
╔════════════════════════════════════════════╗
║            PANDUAN PERMAINAN              ║
╚════════════════════════════════════════════╝

PERINTAH DASAR:
  - BERGERAK: ketik nama arah (utara, selatan, timur, barat, atas, bawah, dll)
  - LIHAT_NPC: bicara dengan NPC di lokasi saat ini
  - EXPLORE: jelajahi lokasi untuk mencari petunjuk
  - STATUS: lihat status pemain
  - PETA: tampilkan peta wilayah
  - LIHAT_CLUE: tampilkan semua petunjuk yang ditemukan
  - SIMPAN: simpan game (belum diimplementasi)
  - KELUAR: keluar dari game

TIPS:
  1. Bicara dengan NPC untuk mendapatkan petunjuk dan item penting
  2. Jelajahi semua lokasi untuk mengumpulkan clue
  3. Beberapa item penting dibutuhkan untuk membuka treasure spots
  4. Hati-hati dengan lokasi berbahaya!
  5. Kelola uang Anda dengan bijak

TUJUAN UTAMA:
  Temukan harta karun legendaris di Bantul dan tentukan nasib Anda!
        """)

    def show_map(self):
        """Tampilkan peta Bantul"""
        print("""
╔═══════════════════════════════════════════════════╗
║        PETA WILAYAH PENCARIAN BANTUL             ║
╚═══════════════════════════════════════════════════╝

                    UTARA
                      ▲
                      │
    [PUNCAK GUNUNG]   │   [CANDI PRAMBANAN]
           │            │         ▲
           │         [JEJERAN]────┤
           │            │         │
    [DESA KULON]◄─[JALAN UTAMA]─►[PASAR]
           │            │
           │     [BANDARA]──────────►[GUA MISTERI]
           │                              ▼
           │                        [DALAM GUA]
        ◄──┴─────────────────────────────────────►
                    SELATAN

LOKASI PENTING:
  🏛️  Candi Prambanan: Tempat suci dengan petunjuk
  🏔️  Puncak Gunung: Batu bertulis kuno
  🕳️  Gua Misteri: Kemungkinan lokasi harta karun
  🏘️  Desa Kulon: Memperoleh clue dari kepala desa
  🏪 Pasar Tradisional: Penjual peta kuno
  🪦  Makam Raja: Lokasi harta karun tersembunyi
        """)

    def show_clues(self):
        """Tampilkan semua petunjuk"""
        print(f"\n{'='*50}")
        print("🔍 PETUNJUK YANG TELAH DITEMUKAN:")
        print(f"{'='*50}")
        
        if not self.clues_found:
            print("   Belum ada petunjuk ditemukan. Jelajahi dan bicara dengan NPC!")
        else:
            for i, clue in enumerate(self.clues_found, 1):
                print(f"{i}. {clue}")

    def handle_movement(self, direction: str):
        """Handle pergerakan pemain"""
        exits = self.locations[self.current_location].get('exits', {})
        
        if direction not in exits:
            print(f"❌ Tidak bisa pergi ke {direction} dari sini!")
            return
        
        next_location = exits[direction]
        self.current_location = next_location
        
        # Simulasi travel
        print(f"\n🚶 Anda berjalan ke {direction}...")
        time.sleep(1)
        
        # Random encounter di tempat berbahaya
        if self.locations[next_location].get('danger'):
            if random.random() > 0.5:
                damage = random.randint(10, 25)
                self.health -= damage
                print(f"⚠️  Anda terpeleset dan terluka! -{damage}% kesehatan")
                
                if self.health <= 0:
                    self.end_game_bad("Anda terlalu terluka dan harus dilarikan ke rumah sakit!")
                    return
        
        self.show_location()

    def main_game_loop(self):
        """Loop utama permainan"""
        self.show_location()
        
        while not self.game_over:
            self.show_status()
            self.show_exits()
            
            command = self.get_player_input("Perintah Anda")
            
            # Perintah gerakan
            if command in self.locations[self.current_location].get('exits', {}):
                self.handle_movement(command)
                continue
            
            # Perintah lainnya
            if command == "lihat_npc":
                self.interact_with_npc()
            elif command == "explore":
                self.explore_location()
            elif command == "status":
                self.show_status()
            elif command == "peta":
                self.show_map()
            elif command == "lihat_clue":
                self.show_clues()
            elif command == "perintah":
                self.show_help()
            elif command == "keluar":
                confirm = input("Anda yakin ingin keluar? (y/n) ")
                if confirm.lower() == 'y':
                    self.end_game_exit()
                    break
            else:
                print("❌ Perintah tidak dikenali. Ketik 'perintah' untuk bantuan.")

    def end_game_bad(self, reason: str):
        """Game over - ending buruk"""
        self.game_over = True
        print(f"\n💀 GAME OVER 💀")
        print(f"   {reason}")
        print(f"   Anda tidak berhasil menemukan harta karun...")

    def end_game_exit(self):
        """Game over - pemain keluar"""
        self.game_over = True
        print("\n👋 Terima kasih sudah bermain The Mystery Adventure Bot!")
        print(f"   Anda mengunjungi {len(self.visited_locations)} lokasi")
        print(f"   Anda menemukan {len(self.clues_found)} petunjuk")

    def show_ending(self):
        """Tampilkan ending"""
        if not self.treasure_found:
            return
        
        ending = self.game_state.get('ending', 'greedy')
        
        if ending == 'greedy':
            print(f"""
╔═══════════════════════════════════════════════════╗
║         ENDING 1: SI KAYA YANG SERAKAH            ║
╚═══════════════════════════════════════════════════╝

Dengan rakus, Anda mengambil semua harta karun!
Total kekayaan: Rp {self.money:,}

Anda menjadi kaya raya, namun ketenangan hati Anda hilang.
Setiap malam Anda bermimpi tentang kutukan leluhur...

Namun, beberapa tahun kemudian, Anda menggunakan sebagian
kekayaan untuk membangun museum sejarah dan pendidikan.
Mungkin pada akhirnya, hati nurani Anda berbicara...

★★★★☆ Rating: 4/5 Bintang
            """)
        
        elif ending == 'balanced':
            print(f"""
╔═══════════════════════════════════════════════════╗
║        ENDING 2: PETUALANG YANG BIJAKSANA         ║
╚═══════════════════════════════════════════════════╝

Anda mengambil sebagian harta dengan bijak!
Total kekayaan: Rp {self.money:,}

Anda meninggalkan sebagian harta untuk pemerintah sebagai
pelestarian warisan budaya. Masyarakat lokal menganggap Anda
sebagai pahlawan yang berbudi luhur.

Dengan uang yang Anda miliki, Anda membuka sekolah sejarah
dan mempromosikan pariwisata budaya di Bantul.

Ibu kota memberi Anda penghargaan bergengsi!

★★★★★ Rating: 5/5 Bintang
            """)
        
        elif ending == 'hero':
            print(f"""
╔═══════════════════════════════════════════════════╗
║           ENDING 3: PAHLAWAN SEJATI              ║
╚═══════════════════════════════════════════════════╝

Anda melaporkan penemuan ini ke pemerintah!
Reward dari pemerintah: Rp {self.money:,}

"Anda adalah pahlawan!" kata gubernur Yogyakarta sambil
memberikan medali penghargaan.

Pemerintah mendirikan museum penting dengan nama Anda.
Harta karun dirawat dengan baik untuk generasi mendatang.

Anda dikenal di seluruh Indonesia sebagai petualang yang
berpikiran mulia dan mempunyai integritas tinggi!

Dunia pun mengenali dedikasi Anda terhadap preservasi budaya!

★★★★★ Rating: 5/5 Bintang (100% ACHIEVEMENT UNLOCKED)
            """)

def main():
    """Fungsi utama"""
    game = MysteryAdventureGame()
    
    try:
        game.start_game()
    except KeyboardInterrupt:
        print("\n\n👋 Permainan dihentikan. Terima kasih sudah bermain!")
    
    if game.treasure_found:
        game.show_ending()
    
    print("\n" + "="*55)
    print("Terima kasih telah memainkan The Mystery Adventure Bot!")
    print("Kunjungi Bantul dan jelajahi keindahan budaya Indonesia!")
    print("="*55 + "\n")

if __name__ == "__main__":
    main()
