return {
  {
    "stevearc/conform.nvim",
    opts = require "configs.conform",
  },
  {
    "tpope/vim-sleuth"
  },
  {
    "Bilal2453/luvit-meta",
    lazy = true
  },
  {
    "folke/lazydev.nvim",
    ft = "lua",
    opts = {
      library = {
        { path = "luvit-meta/library", words = { "vim%.uv" } }
      }
    }
  },
  {
    "scrooloose/nerdtree",
    config = function()
      vim.g.NerdTreeCustomOpenArgs = { file = { where = "t" } }
    end,
  },
  {
    "nvim-telescope/telescope.nvim",
    event = "VimEnter",
    branch = "0.1.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      {
        "nvim-telescope/telescope-fzf-native.nvim",
        build = function()
          if vim.fn.executable("gmake") == 1 then
            return "gmake"
          else
            return "make"
          end
        end,
        cont = function()
          return vim.fn.executable("make") == 1
        end,
      },
      { "nvim-telescope/telescope-ui-select.nvim" },
      { "nvim-tree/nvim-web-devicons", enabled = vim.g.have_nerd_font },
    },
    config = function()
      pcall(require("telescope").load_extension, "fzf")
      pcall(require("telescope").load_extension, "ui-select")

      local builtin = require("telescope.builtin")
      -- TODO: set keybindings - import from mappings.lua?
      vim.keymap.set('n', '<leader>pf', builtin.find_files, {})
      -- vim.keymap.set('n', '<leader>pf', builtin.find_files, {})
      vim.keymap.set('n', '<leader>ps', function()
        builtin.grep_string({ search = vim.fn.input("Grep > ") })
      end)
    end,
  },
  {
    "nvim-treesitter/nvim-treesitter"
  },
  -- {
  --   "williamboman/mason.nvim",
  --   config = function()
  --     require("mason").setup()
  --   end
  -- },
  -- {
  --   "williamboman/mason-lspconfig.nvim",
  --   opts = {
  --     auto_install = true
  --   }
  -- },
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "williamboman/mason.nvim",
      "williamboman/mason-lspconfig.nvim",
      "WhoIsSethDaniel/mason-tool-installer.nvim",
    },
    config = function()
      require "configs.lspconfig"
    end,
  },
}
