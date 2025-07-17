import {sveltekit} from '@sveltejs/kit/vite';
import {defineConfig} from 'vite';
import path from "path";

const isDocker = process.env.DOCKER === 'true';

export default defineConfig({
    plugins: [sveltekit()],
    server: {
        fs: {
            allow: [
                path.resolve(__dirname, './3rdparty'),
            ]
        },
        proxy: {
            '/api': {
                target: isDocker ? 'http://api:8000' : 'http://localhost:8000',
                changeOrigin: true,
                rewrite: path => path.replace(/^\/api/, ''),
            },
        },
    }
});
