#include "brotli/decode.h"
#include "brotli/encode.h"

int main() {
    return (
    	BrotliDecoderVersion() == 0x1000007 && 
    	BrotliEncoderVersion() == 0x1000007
    ) ? 0 : -1;
}
