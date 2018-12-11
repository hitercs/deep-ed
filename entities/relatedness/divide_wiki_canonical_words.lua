
if not opt then
  cmd = torch.CmdLine()
  cmd:option('-root_data_dir', '', 'Root path of the data, $DATA_PATH.')
  cmd:option('-entities', 'Partition','Set of entities for which we train embeddings: 4EX (tiny, for debug) | ' .. 
  'RLTD (restricted set) | ALL (all Wiki entities, too big to fit on a single GPU) | Partition (paritions of all Wiki entities, guarantee each partition can be fit in single GPU)')
  cmd:option('-part_id', 1, 'Partition ID for training ALL entities')
  cmd:text()
  opt = cmd:parse(arg or {})
  assert(opt.root_data_dir ~= '', 'Specify a valid root_data_dir path argument.')  
end


dofile 'utils/utils.lua'
dofile 'entities/relatedness/relatedness.lua'
dofile 'entities/ent_name2id_freq/ent_name_id.lua'

input = opt.root_data_dir .. 'generated/wiki_canonical_words.txt'

output = opt.root_data_dir .. 'generated/partition/wiki_canonical_words_part' .. opt.part_id .. '.txt'
ouf = assert(io.open(output, "w"))

print('\nStarting dataset filtering.')

local cnt = 0
for line in io.lines(input) do
  cnt = cnt + 1
  if cnt % 500000 == 0 then
    print('    =======> processed ' .. cnt .. ' lines')
  end

  local parts = split(line, '\t')
  assert(table_len(parts) == 3)

  local ent_wikiid = tonumber(parts[1])
  local ent_name = parts[2]
  assert(ent_wikiid)
  
  if is_valid_ent(ent_wikiid) then
    ouf:write(line .. '\n')
  end  
end  

ouf:flush() 
io.close(ouf)
