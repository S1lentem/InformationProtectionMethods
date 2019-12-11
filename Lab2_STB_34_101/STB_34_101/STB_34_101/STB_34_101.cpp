#include <string>
#include <iostream>
#include <bitset>
#include <array>
#include <istream>
#include <fstream>
const std::array<std::bitset<8>, 256> H{
	0xB1, 0x94, 0xBA, 0xC8, 0x0A, 0x08, 0xF5, 0x3B, 0x36, 0x6D, 0x00, 0x8E, 0x58, 0x4A, 0x5D, 0xE4,
	0x85, 0x04, 0xFA, 0x9D, 0x1B, 0xB6, 0xC7, 0xAC, 0x25, 0x2E, 0x72, 0xC2, 0x02, 0xFD, 0xCE, 0x0D,
	0x5B, 0xE3, 0xD6, 0x12, 0x17, 0xB9, 0x61, 0x81, 0xFE, 0x67, 0x86, 0xAD, 0x71, 0x6B, 0x89, 0x0B,
	0x5C, 0xB0, 0xC0, 0xFF, 0x33, 0xC3, 0x56, 0xB8, 0x35, 0xC4, 0x05, 0xAE, 0xD8, 0xE0, 0x7F, 0x99,
	0xE1, 0x2B, 0xDC, 0x1A, 0xE2, 0x82, 0x57, 0xEC, 0x70, 0x3F, 0xCC, 0xF0, 0x95, 0xEE, 0x8D, 0xF1,
	0xC1, 0xAB, 0x76, 0x38, 0x9F, 0xE6, 0x78, 0xCA, 0xF7, 0xC6, 0xF8, 0x60, 0xD5, 0xBB, 0x9C, 0x4F,
	0xF3, 0x3C, 0x65, 0x7B, 0x63, 0x7C, 0x30, 0x6A, 0xDD, 0x4E, 0xA7, 0x79, 0x9E, 0xB2, 0x3D, 0x31,
	0x3E, 0x98, 0xB5, 0x6E, 0x27, 0xD3, 0xBC, 0xCF, 0x59, 0x1E, 0x18, 0x1F, 0x4C, 0x5A, 0xB7, 0x93,
	0xE9, 0xDE, 0xE7, 0x2C, 0x8F, 0x0C, 0x0F, 0xA6, 0x2D, 0xDB, 0x49, 0xF4, 0x6F, 0x73, 0x96, 0x47,
	0x06, 0x07, 0x53, 0x16, 0xED, 0x24, 0x7A, 0x37, 0x39, 0xCB, 0xA3, 0x83, 0x03, 0xA9, 0x8B, 0xF6,
	0x92, 0xBD, 0x9B, 0x1C, 0xE5, 0xD1, 0x41, 0x01, 0x54, 0x45, 0xFB, 0xC9, 0x5E, 0x4D, 0x0E, 0xF2,
	0x68, 0x20, 0x80, 0xAA, 0x22, 0x7D, 0x64, 0x2F, 0x26, 0x87, 0xF9, 0x34, 0x90, 0x40, 0x55, 0x11,
	0xBE, 0x32, 0x97, 0x13, 0x43, 0xFC, 0x9A, 0x48, 0xA0, 0x2A, 0x88, 0x5F, 0x19, 0x4B, 0x09, 0xA1,
	0x7E, 0xCD, 0xA4, 0xD0, 0x15, 0x44, 0xAF, 0x8C, 0xA5, 0x84, 0x50, 0xBF, 0x66, 0xD2, 0xE8, 0x8A,
	0xA2, 0xD7, 0x46, 0x52, 0x42, 0xA8, 0xDF, 0xB3, 0x69, 0x74, 0xC5, 0x51, 0xEB, 0x23, 0x29, 0x21,
	0xD4, 0xEF, 0xD9, 0xB4, 0x3A, 0x62, 0x28, 0x75, 0x91, 0x14, 0x10, 0xEA, 0x77, 0x6C, 0xDA, 0x1D, };

template<int Size>
void print_hex(const std::bitset<Size>& set, const std::string& end = "\n")
{
	for (auto i = 0; i < Size / 8; i++)
	{
		char d =
			((set[i * 8 + 4] ? 1 : 0) << 0) |
			((set[i * 8 + 5] ? 1 : 0) << 1) |
			((set[i * 8 + 6] ? 1 : 0) << 2) |
			((set[i * 8 + 7] ? 1 : 0) << 3);
		d += d < 10 ? '0' : 'A' - 10;
		std::cout << d;
		d =
			((set[i * 8 + 0] ? 1 : 0) << 0) |
			((set[i * 8 + 1] ? 1 : 0) << 1) |
			((set[i * 8 + 2] ? 1 : 0) << 2) |
			((set[i * 8 + 3] ? 1 : 0) << 3);
		d += d < 10 ? '0' : 'A' - 10;
		std::cout << d;
	}
	std::cout << end;
}

template<int Size>
std::bitset<Size> hex_to_set(const std::string& hex)
{
	std::bitset<Size> res;
	auto text(hex);
	const int byte = (hex.size() + 1) / 2;
	text.resize(byte * 2, '\0');
	for (auto i = 0; i < byte * 2; i += 2) {
		std::swap(text[i], text[i + 1]);
	}

	for (auto i = 0; i < byte * 2 && i < Size / 4; i++) {
		auto d = text[i];
		d -= d <= '9' ? '0' : 'A' - 10;
		for (auto j = 0; j < 4; j++)
			res[i * 4 + j] = (d & (1 << j));
	}
	return res;
}

template<int Size>
std::string set_to_hex_string(const std::bitset<Size> set) {
	std::string res(Size / 4, '\0');
	for (auto i = 0; i < Size / 4; i++) {
		char d =
			((set[i * 4 + 0] ? 1 : 0) << 0) |
			((set[i * 4 + 1] ? 1 : 0) << 1) |
			((set[i * 4 + 2] ? 1 : 0) << 2) |
			((set[i * 4 + 3] ? 1 : 0) << 3);
		d += d < 10 ? '0' : 'A' - 10;
		res[i] = d;
	}
	for (auto i = 0; i < Size / 4; i += 2) {
		std::swap(res[i], res[i + 1]);
	}
	return res;
}


template<int Size>
std::string set_to_string(const std::bitset<Size> bs, const int res_bytes = -1) {
	const auto cnt = res_bytes == -1 ? Size / 8 : res_bytes;
	std::string res(cnt, '\0');
	for (auto i = 0; i < cnt; i++) {
		for (auto j = 0; j < 8; j++) {
			res[i] |= ((bs[i * 8 + j] ? 1 : 0) << j);
		}
	}
	return res;
}

template<int Size>
static std::bitset<Size> string_to_set(const std::string& str)
{
	std::bitset<Size> res;
	auto byte_count = Size / 8;
	if (str.size() < byte_count)
		byte_count = str.size();
	for (auto i = 0; i < byte_count; i++)
	{
		for (int j = 0; j < 8; j++)
			res[i * 8 + j] = str[i] & (1 << j);
	}
	return res;
}

template<int Size>
std::bitset<Size> rotl(const std::bitset<Size>& bs, int n) {
	return (bs << n) | (bs >> (Size - n));
}

std::bitset<32> G(std::bitset<32> u, int r) {
	std::bitset<8> byte;
	std::bitset<32> sum;
	for (auto i = 0; i < 4; i++) {
		for (auto j = 0; j < 8; j++)
			byte[j] = u[i * 8 + j];
		byte = H[byte.to_ulong()];
		for (auto j = 0; j < 8; j++)
			sum[i * 8 + j] = byte[j];
	}
	return rotl(sum, r);
}


std::bitset<128> f(const std::bitset<128>& x, const std::bitset<256>& tetta) {
	std::array<std::bitset<32>, 8> keys;
	std::bitset<128> y;
	for (auto i = 0; i < 8; i++) {
		for (auto j = 0; j < 32; j++) {
			keys[i][j] = tetta[i * 32 + j];
		}
	}
	std::bitset<32> a, b, c, d;
	for (auto i = 0; i < 32; i++) {
		a[i] = x[i];
		b[i] = x[32 + i];
		c[i] = x[64 + i];
		d[i] = x[96 + i];
	}
	for (auto i = 1; i <= 8; i++) {
		b ^= G(a.to_ulong() + keys[(7 * i - 7) % 8].to_ulong(), 5);
		c ^= G(d.to_ulong() + keys[(7 * i - 6) % 8].to_ulong(), 21);
		a = a.to_ulong() - (G(b.to_ulong() + keys[(7 * i - 5) % 8].to_ulong(), 13).to_ulong());
		std::bitset<32> e = G(b.to_ulong() + c.to_ulong() + keys[(7 * i - 4) % 8].to_ulong(), 21) ^ std::bitset<32>(i);
		b = b.to_ulong() + e.to_ulong();
		c = c.to_ulong() - e.to_ulong();
		d = d.to_ulong() + G(c.to_ulong() + keys[(7 * i - 3) % 8].to_ulong(), 13).to_ulong();
		b ^= G(a.to_ulong() + keys[(7 * i - 2) % 8].to_ulong(), 21);
		c ^= G(d.to_ulong() + keys[(7 * i - 1) % 8].to_ulong(), 5);
		std::swap(a, b);
		std::swap(c, d);
		std::swap(b, c);
	}
	for (int i = 0; i < 32; i++) {
		y[i] = b[i];
		y[32 + i] = d[i];
		y[64 + i] = a[i];
		y[96 + i] = c[i];
	}
	return y;
}

std::bitset<128> F_1(const std::bitset<128>& x, const std::bitset<256>& tetta) {
	std::array<std::bitset<32>, 8> keys;
	for (auto i = 0; i < 8; i++) {
		for (auto j = 0; j < 32; j++) {
			keys[i][j] = tetta[i * 32 + j];
		}
	}
	std::bitset<32> a, b, c, d, e;
	for (auto i = 0; i < 32; i++) {
		a[i] = x[i];
		b[i] = x[32 + i];
		c[i] = x[64 + i];
		d[i] = x[96 + i];
	}

	for (auto i = 8; i >= 1; i--) {
		b ^= G(a.to_ulong() + keys[(7 * i - 1) % 8].to_ulong(), 5);
		c ^= G(d.to_ulong() + keys[(7 * i - 2) % 8].to_ulong(), 21);
		a = a.to_ulong() - G(b.to_ulong() + keys[(7 * i - 3) % 8].to_ulong(), 13).to_ulong();
		e = G(b.to_ulong() + c.to_ulong() + keys[(7 * i - 4) % 8].to_ulong(), 21) ^ std::bitset<32>(i);
		b = b.to_ulong() + e.to_ulong();
		c = c.to_ulong() - e.to_ulong();
		d = d.to_ulong() + G(c.to_ulong() + keys[(7 * i - 5) % 8].to_ulong(), 13).to_ulong();
		b ^= G(a.to_ulong() + keys[(7 * i - 6) % 8].to_ulong(), 21);
		c ^= G(d.to_ulong() + keys[(7 * i - 7) % 8].to_ulong(), 5);
		std::swap(a, b);
		std::swap(c, d);
		std::swap(a, d);
	}
	std::bitset<128> y;
	for (auto i = 0; i < 32; i++) {
		y[i] = c[i];
		y[32 + i] = a[i];
		y[64 + i] = d[i];
		y[96 + i] = b[i];
	}
	return y;
}

std::string simple_replace(
	const std::string& text,
	const std::bitset<256>& key,
	std::bitset<128>(*fun)(const std::bitset<128>&, const std::bitset<256>&))
{
	const int n = (text.size() + 15) / 16;
	std::string res;
	auto n_shift = 0;
	int m = text.size() % 16;
	if (m) n_shift = -2;
	;
	for (auto i = 0; i < n + n_shift; i++) {
		const auto y = fun(string_to_set<128>(text.substr(i * 16, 16)), key);
		res += set_to_string(y);
	}
	if (n_shift == -2) {
		auto r = fun(string_to_set<128>(text.substr((n - 2) * 16, 16)), key);
		auto x_n = string_to_set<128>(text.substr((n - 1) * 16)); 
		for (auto i = m * 8; i < 128; i++)
			x_n[i] = r[i];
		x_n = fun(x_n, key);
		res += set_to_string(x_n);
		res += set_to_string(r, m);
	}
	return res;
}

std::string gamming_encrypt(
	const std::string& text,
	std::bitset<256>& key, std::bitset<128>& s,
	std::bitset<128>(*fun)(const std::bitset<128>&, const std::bitset<256>&))
{
	const int n = (text.size() + 15) / 16;
	std::string res;
	int n_shift = 0, m = text.size() % 16;
	if (m) n_shift = -1;
	std::bitset<128> y = s, x;
	for (auto i = 0; i < n + n_shift; i++) {
		x = string_to_set<128>(text.substr(i * 16, 16));
		y = x ^ fun(y, key);
		res += set_to_string(y);
	}
	if (n_shift == -1) {
		x = string_to_set<128>(text.substr((n - 1) * 16));
		y = x ^ fun(y, key);
		res += set_to_string(y, m);
	}
	return res;
}

std::string gamming_decrypt(
	const std::string& text,
	std::bitset<256>& key, std::bitset<128>& s,
	std::bitset<128>(*fun)(const std::bitset<128>&, const std::bitset<256>&))
{
	const int n = (text.size() + 15) / 16;
	std::string res;
	int n_shift = 0, m = text.size() % 16;
	if (m) n_shift = -1;
	std::bitset<128> y, x = s, x1;
	for (auto i = 0; i < n + n_shift; i++) {
		x1 = string_to_set<128>(text.substr(i * 16, 16));
		y = x1 ^ fun(x, key);
		res += set_to_string(y);
		x = x1;
	}
	if (n_shift == -1) {
		x1 = string_to_set<128>(text.substr((n - 1) * 16));
		y = x1 ^ fun(x, key);
		res += set_to_string(y, m);
	}
	return res;
}

template<int Size>
std::bitset<Size> bitset_inc(const std::bitset<Size>& bs) {
	std::bitset<Size> res(bs);
	for (auto i = 0; i < Size; i++) {
		if (!res[i]) {
			res[i] = 1;
			break;
		}
		res[i] = 0;
	}
	return res;
}

std::string counter(
	const std::string& text,
	std::bitset<256>& key, std::bitset<128>& s,
	std::bitset<128>(*fun)(const std::bitset<128>&, const std::bitset<256>&))
{
	int n = (text.size() + 15) / 16;
	std::string res;
	int n_shift = 0, m = text.size() % 16;
	if (m) n_shift = -1;
	std::bitset<128> y, ss = fun(s, key), x;
	for (auto i = 0; i < n + n_shift; i++) {
		ss = bitset_inc(ss);
		x = string_to_set<128>(text.substr(i * 16, 16));
		y = x ^ fun(ss, key);
		res += set_to_string(y);
	}
	if (n_shift == -1) {
		ss = bitset_inc(ss);
		x = string_to_set<128>(text.substr((n - 1) * 16));
		y = x ^ fun(ss, key);
		res += set_to_string(y, m);
	}
	return res;
}


int main() {
	auto t = hex_to_set<256>("E9DEE72C8F0C0FA62DDB49F46F73964706075316ED247A3739CBA38303A98BF6");
	auto s = hex_to_set<128>("7ECDA4D01544AF8CA58450BF66D2E88A");

	const auto mode = 0;
	auto const enc = 0;

	const std::string input_text = "BSUIR135BSUIR135BSUIR135BSUIR135BSUIR135BSUIR135";

	std::bitset<128>(*fun)(const std::bitset<128>&, const std::bitset<256>&);
	auto output_text = simple_replace(input_text, t, f);
	auto result = simple_replace(output_text, t, F_1);

	std::cout << input_text << std::endl;
	for (auto i : output_text)
	{
		std::cout << std::hex << int(static_cast<unsigned char>(i));
	}
	std::cout << std::endl << result << std::endl << std::endl << std::endl;

	output_text = gamming_encrypt(input_text, t, s, f);
	result = gamming_decrypt(output_text, t, s, f);
	std::cout << input_text << std::endl;
	for (auto i : output_text)
	{
		std::cout << std::hex << int(static_cast<unsigned char>(i));
	}
	std::cout << std::endl << result << std::endl << std::endl << std::endl;

	return 0;
}
