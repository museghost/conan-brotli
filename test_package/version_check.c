#include "brotli/decode.h"
#include "brotli/encode.h"

int main() {
    return (
    	BrotliDecoderVersion() == 0x1000004 && 
    	BrotliEncoderVersion() == 0x1000004
    ) ? 0 : -1;
}
