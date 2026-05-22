function add(a, b)
  return a + b
end

function double(x)
  return x * 2
end

local r number = add(3, 4)
print(r)
local s number = double(r)
print(s)
print(add(10, add(1, 2)))
