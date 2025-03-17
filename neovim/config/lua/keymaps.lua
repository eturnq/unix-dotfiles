vim.keymap.set("n", "<C-n>", ":Neotree filesystem reveal left toggle<CR>")
vim.keymap.set("n", "<leader>e", ":Neotree focus<CR>")
vim.keymap.set("n", "<leader>pf", ":Telescope find_files<CR>")
vim.keymap.set("n", "<leader>th", ":Telescope colorscheme<CR>")
vim.keymap.set("n", "<leader>ft", vim.lsp.buf.format, {})

vim.keymap.set("n", "<tab>", ":BufferLineCycleNext<CR>")
vim.keymap.set("n", "<S-tab>", ":BufferLineCyclePrev<CR>")
