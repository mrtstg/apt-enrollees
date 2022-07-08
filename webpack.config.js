const path = require('path')

module.exports = {
	mode: 'development',
	cache: {
		type: 'filesystem'
	},
	output: {
		path: path.resolve(__dirname, 'dist'),
		filename: '[name].bundle.js'
	},
	entry: ['./src/js/index.js'],
	resolve: {
		alias: {
			svelte: path.resolve('node_modules', 'svelte')
		},
		extensions: ['.mjs', '.js', '.svelte'],
		mainFields: ['svelte', 'browser', 'module', 'main']
	},
	module: {
		rules: [
		{
			test: /\.(html|svelte)$/,
			use: 'svelte-loader'
		},
		{
			test: /node_modules\/svelte\/.*\.mjs$/,
			resolve: {
				fullySpecified: false
			}
		}
		]
	}
}