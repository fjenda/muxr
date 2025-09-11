/**
 * Utility function to get the MIME type of audio file based on its extension.
 * @param filePath - The path of the audio file.
 */
export const getMimeType = (filePath: string): string => {
	const ext = filePath.split('.').pop()?.toLowerCase();
	switch (ext) {
		case 'mp3':
			return 'audio/mpeg';
		case 'wav':
			return 'audio/wav';
		case 'ogg':
			return 'audio/ogg';
		case 'flac':
			return 'audio/flac';
		case 'aac':
			return 'audio/aac';
		case 'm4a':
			return 'audio/mp4';
		default:
			return 'audio/*';
	}
};
