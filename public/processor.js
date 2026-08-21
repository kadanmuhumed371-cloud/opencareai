class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.buffer = [];
        this.chunkSize = 1024; // Accumulate ~64ms of audio at 16kHz
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (input && input.length > 0) {
            const channelData = input[0];
            
            // If the audio context sample rate is not 16000, downsample to 16000Hz Mono PCM
            const sourceSampleRate = sampleRate; // Global sampleRate in AudioWorkletGlobalScope
            if (sourceSampleRate !== 16000) {
                const ratio = sourceSampleRate / 16000;
                let newLength = Math.round(channelData.length / ratio);
                for (let i = 0; i < newLength; i++) {
                    let index = Math.min(channelData.length - 1, Math.round(i * ratio));
                    this.buffer.push(channelData[index]);
                }
            } else {
                for (let i = 0; i < channelData.length; i++) {
                    this.buffer.push(channelData[i]);
                }
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