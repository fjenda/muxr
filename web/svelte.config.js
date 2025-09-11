import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import path from 'path';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({
			fallback: 'index.html'
		}),
		alias: {
			$components: './src/lib/components',
			$dialogs: './src/lib/dialogs',
			$providers: './src/lib/providers',
			$stores: './src/lib/stores',
			$utils: './src/lib/utils',
			'@multitrack': path.resolve('./3rdparty/wavesurfer-multitrack/src')
		}
	}
};

export default config;
