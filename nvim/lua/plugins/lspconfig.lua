return {
	{
		"williamboman/mason.nvim",
		config = function()
			require("mason").setup()
		end
	},

	{
		"neovim/nvim-lspconfig",
		config = function()
			local capabilities = require('cmp_nvim_lsp').default_capabilities()
			local lspconfig = require("lspconfig")

			lspconfig.gopls.setup{
				capabilities = capabilities
			}

			lspconfig.pyright.setup{
				capabilities = capabilities
			}
		end
	}
}
