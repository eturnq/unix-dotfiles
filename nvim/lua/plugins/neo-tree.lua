return {
	"nvim-neo-tree/neo-tree.nvim",
	branch = "v3.x",
	opts = {
		filesystem = {
			filtered_items = {
				visible = true,
				show_hidden_count = true,
				hide_dotfile = false,
				hide_gitignored = false,
				never_show = {},
			}
		}
	},
	dependencies = {
		"nvim-lua/plenary.nvim",
		"nvim-tree/nvim-web-devicons",
		"MunifTanjim/nui.nvim",
		-- "3rd/image.nvim", -- Image support in preview window
	}
}
