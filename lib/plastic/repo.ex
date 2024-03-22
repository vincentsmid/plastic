defmodule Plastic.Repo do
  use Ecto.Repo,
    otp_app: :plastic,
    adapter: Ecto.Adapters.Postgres
end
