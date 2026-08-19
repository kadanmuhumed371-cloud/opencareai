class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.buffer = [];
        this.chunkSize = 2048; // Accumulate ~128ms of audio at 16kHz
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (input && input.length > 0) {
            const channelData = input[0];
            for (let i = 0; i < channelData.length; i++) {
                this.buffer.push(channelData[i]);
            }

            if (this.buffer.length >= this.chunkSize) {
                const pcm16Data = new Int16Array(this.buffer.length);
                for (let i = 0; i < this.buffer.length; i++) {
                    let val = Math.max(-1, Math.min(1, this.buffer[i]));
                    pcm16Data[i] = val < 0 ? val * 0x8000 : val * 0x7FFF;
                }
                this.port.postMessage(pcm16Data.buffer, [pcm16Data.buffer]);
                this.buffer = [];
            }
        }
        return true;
    }
}

registerProcessor('audio-processor', AudioProcessor);